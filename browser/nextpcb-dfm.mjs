#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

function usage() {
  return "usage: nextpcb-dfm.mjs --archive FILE --output FILE --backend browserbase|local [--chrome FILE] [--timeout SECONDS]";
}

function parseArgs(argv) {
  const args = { timeout: 180, backend: "local" };
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (key === "--help") return { help: true };
    if (!["--archive", "--output", "--backend", "--chrome", "--timeout"].includes(key)) {
      throw new Error(`unknown argument: ${key}`);
    }
    const value = argv[index + 1];
    if (!value) throw new Error(`missing value for ${key}`);
    args[key.slice(2)] = value;
    index += 1;
  }
  for (const key of ["archive", "output", "backend"]) {
    if (!args[key]) throw new Error(`missing --${key}`);
  }
  if (!["browserbase", "local"].includes(args.backend)) {
    throw new Error("--backend must be browserbase or local");
  }
  if (args.backend === "local" && !args.chrome) throw new Error("missing --chrome for local backend");
  args.timeout = Number(args.timeout);
  if (!Number.isFinite(args.timeout) || args.timeout <= 0) {
    throw new Error("--timeout must be a positive number");
  }
  return args;
}

function sanitizeError(error) {
  return String(error)
    .replace(/(?:wss|ws|https):\/\/[^\s"']+/g, "<redacted-url>")
    .replace(/[A-Za-z0-9_-]{40,}/g, "<redacted-token>");
}

async function retrieveBrowserbaseReport(apiKey, sessionId, output, timeout) {
  const deadline = Date.now() + timeout;
  while (Date.now() < deadline) {
    const query = new URLSearchParams({
      sessionId,
      mimeType: "application/pdf",
      minSize: "1024",
      limit: "10",
    });
    const listed = await fetch(`https://api.browserbase.com/v1/downloads?${query}`, {
      headers: { "X-BB-API-Key": apiKey },
    });
    if (!listed.ok) throw new Error(`Browserbase download listing returned HTTP ${listed.status}`);
    const listing = await listed.json();
    if (listing.total > 0) {
      const download = [...listing.downloads].sort((left, right) =>
        String(right.createdAt).localeCompare(String(left.createdAt))
      )[0];
      const response = await fetch(`https://api.browserbase.com/v1/downloads/${download.id}`, {
        headers: { "X-BB-API-Key": apiKey, Accept: "application/octet-stream" },
      });
      if (!response.ok) throw new Error(`Browserbase download retrieval returned HTTP ${response.status}`);
      fs.writeFileSync(path.resolve(output), Buffer.from(await response.arrayBuffer()));
      const removed = await fetch(`https://api.browserbase.com/v1/downloads/${download.id}`, {
        method: "DELETE",
        headers: { "X-BB-API-Key": apiKey },
      });
      return {
        filename: download.filename,
        size: download.size,
        checksum: download.checksum,
        cloudCleanup: removed.status === 204 ? "pass" : `failed-http-${removed.status}`,
      };
    }
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  throw new Error("Browserbase did not expose the downloaded PDF before timeout");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    console.log(usage());
    return;
  }
  for (const key of ["archive", ...(args.backend === "local" ? ["chrome"] : [])]) {
    if (!fs.statSync(args[key]).isFile()) throw new Error(`${key} is not a file: ${args[key]}`);
  }
  fs.mkdirSync(path.dirname(path.resolve(args.output)), { recursive: true });
  const moduleRoot = path.dirname(fileURLToPath(import.meta.url));
  const { chromium } = await import(path.join(moduleRoot, "node_modules/playwright-core/index.mjs"));
  let browser;
  let context;
  let page;
  let sessionId = null;
  let apiKey = null;
  if (args.backend === "browserbase") {
    apiKey = process.env.BROWSERBASE_API_KEY;
    if (!apiKey) throw new Error("BROWSERBASE_API_KEY is not configured");
    const response = await fetch("https://api.browserbase.com/v1/sessions", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-BB-API-Key": apiKey },
      body: JSON.stringify({ userMetadata: { workflow: "pcb-agent-dfm", provider: "nextpcb" } }),
    });
    if (response.status !== 201) throw new Error(`Browserbase session creation returned HTTP ${response.status}`);
    const session = await response.json();
    sessionId = session.id;
    browser = await chromium.connectOverCDP(session.connectUrl);
    context = browser.contexts()[0];
    page = context.pages()[0] || await context.newPage();
  } else {
    browser = await chromium.launch({ executablePath: args.chrome, headless: true });
    context = await browser.newContext({ acceptDownloads: true });
    page = await context.newPage();
  }
  const timeout = args.timeout * 1000;
  let remoteDownload = null;
  try {
    await page.goto("https://www.nextpcb.com/free-online-gerber-viewer.html", {
      waitUntil: "domcontentloaded",
      timeout,
    });
    const upload = page.locator('input[type="file"]').first();
    await upload.waitFor({ state: "attached", timeout });
    await upload.setInputFiles(path.resolve(args.archive));
    const reportButton = page.getByText("Download Report", { exact: true }).last();
    await reportButton.waitFor({ state: "visible", timeout });
    if (args.backend === "browserbase") {
      const cdp = await context.newCDPSession(page);
      await cdp.send("Browser.setDownloadBehavior", {
        behavior: "allow",
        downloadPath: "downloads",
        eventsEnabled: true,
      });
    }
    const downloadPromise = page.waitForEvent("download", { timeout });
    await reportButton.click();
    const download = await downloadPromise;
    if (args.backend === "browserbase") {
      remoteDownload = await retrieveBrowserbaseReport(apiKey, sessionId, args.output, timeout);
    } else {
      await download.saveAs(path.resolve(args.output));
    }
    console.log(JSON.stringify({
      result: "completed",
      report: path.resolve(args.output),
      backend: args.backend,
      ...(sessionId ? { sessionId } : {}),
      ...(remoteDownload ? { remoteDownload } : {}),
    }));
  } finally {
    await browser.close();
  }
}

main().catch(error => {
  console.error(JSON.stringify({ result: "failed", error: sanitizeError(error) }));
  process.exitCode = 1;
});
