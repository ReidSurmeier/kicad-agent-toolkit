from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
CLI = REPO / "pcb-agent"


class PipelineCliTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(CLI), *args],
            cwd=REPO,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def run_cli_with_env(self, args: list[str], environment: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(CLI), *args],
            cwd=REPO,
            env={**os.environ, **environment},
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def make_dfm_boundaries(self, root: Path, report_text: str) -> tuple[Path, Path]:
        runner = root / "nextpcb-runner"
        runner.write_text(
            "#!/usr/bin/env python3\n"
            "import argparse, hashlib, json, os\n"
            "from pathlib import Path\n"
            "p = argparse.ArgumentParser()\n"
            "p.add_argument('--archive')\n"
            "p.add_argument('--output')\n"
            "p.add_argument('--chrome')\n"
            "p.add_argument('--backend')\n"
            "p.add_argument('--timeout')\n"
            "a = p.parse_args()\n"
            "Path(a.output).write_bytes(b'%PDF-1.4\\n' + b'x' * 2048 + b'\\n%%EOF\\n')\n"
            "if os.environ.get('PCB_AGENT_TEST_MUTATE_ARCHIVE'):\n"
            "    Path(a.archive).write_bytes(Path(a.archive).read_bytes() + b'mutated')\n"
            "payload = {'result': 'completed', 'report': a.output, 'backend': a.backend}\n"
            "if a.backend == 'browserbase':\n"
            "    payload['sessionId'] = 'fixture-session'\n"
            "    checksum = hashlib.sha256(Path(a.output).read_bytes()).hexdigest()\n"
            "    if os.environ.get('PCB_AGENT_TEST_BAD_DOWNLOAD_HASH'): checksum = '0' * 64\n"
            "    payload['remoteDownload'] = {'checksum': checksum, 'size': Path(a.output).stat().st_size, 'cloudCleanup': 'pass'}\n"
            "print(json.dumps(payload))\n"
        )
        runner.chmod(0o755)
        tools = root / "tools"
        tools.mkdir()
        pdftotext = tools / "pdftotext"
        pdftotext.write_text(
            "#!/usr/bin/env python3\n"
            "import sys\n"
            "from pathlib import Path\n"
            f"Path(sys.argv[-1]).write_text({report_text!r})\n"
        )
        pdftotext.chmod(0o755)
        return runner, tools

    def test_help_exposes_the_confirmed_pipeline(self) -> None:
        result = self.run_cli("--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        for command in ("install", "doctor", "validate", "mcp", "release", "dfm"):
            self.assertIn(command, result.stdout)

    def test_dfm_help_exposes_remote_and_local_browser_backends(self) -> None:
        result = self.run_cli("dfm", "--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--browser-backend {auto,browserbase,local}", result.stdout)

    def test_validate_reports_a_machine_readable_repository_pass(self) -> None:
        result = self.run_cli("validate", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "pass")
        self.assertEqual(
            report["skills"],
            ["kicad-design-review", "kicad-pcb-design", "kicad-toolchain-setup"],
        )
        self.assertEqual(report["mcp"]["version"], "2.6.0")
        self.assertEqual(report["mcp"]["commit"], "3ab354ca891e905dcc987219845e4a93c2167f85")
        self.assertEqual(report["mcp"]["upstream_commit"], "ccabbf0daff0db6e902e39d39ea734b018cd3eae")
        self.assertEqual(report["mcp"]["production_vulnerabilities"], 0)
        self.assertEqual(report["browser_automation"]["playwright_core"], "1.61.1")
        self.assertEqual(report["browser_automation"]["production_vulnerabilities"], 0)

    def test_validate_rejects_an_incomplete_skill_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            broken = Path(temporary)
            skill = broken / "skills" / "broken-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: broken-skill\n---\n")

            result = self.run_cli("validate", "--repo", str(broken), "--json")

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "fail")
        self.assertIn("incomplete skill: broken-skill", report["failures"])

    def test_doctor_reports_the_full_stack_without_printing_secrets(self) -> None:
        sentinel = "never-print-this-secret"
        result = self.run_cli_with_env(
            ["doctor", "--json"],
            {
                "BROWSERBASE_API_KEY": "",
                "JLCPCB_APP_ID": "configured-app",
                "JLCPCB_API_KEY": "configured-key",
                "JLCPCB_API_SECRET": sentinel,
            },
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn(sentinel, result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "pass")
        self.assertEqual(report["credentials"]["jlcpcb"], "configured")
        self.assertEqual(report["credentials"]["browserbase"], "not configured")
        for tool in (
            "codex",
            "docker",
            "gerbv",
            "gitnexus",
            "kicad-cli",
            "node",
            "npm",
            "pdftotext",
            "pygerber",
            "python3",
        ):
            self.assertEqual(report["tools"][tool]["status"], "pass", tool)
        self.assertEqual(report["mcp"]["build"], "pass")
        self.assertEqual(report["mcp"]["codex_registration"], "pass")
        self.assertEqual(report["dfm_browser"]["runner"], "pass")
        self.assertEqual(report["dfm_browser"]["playwright_core"], "pass")

    def test_install_dry_run_describes_the_full_pipeline_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / "codex-home"
            result = self.run_cli(
                "install",
                "--codex-home",
                str(codex_home),
                "--dry-run",
                "--json",
            )

            self.assertFalse(codex_home.exists())

        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "pass")
        self.assertEqual(report["mode"], "dry-run")
        self.assertEqual(
            report["skills"],
            ["kicad-design-review", "kicad-pcb-design", "kicad-toolchain-setup"],
        )
        self.assertIn("KiCAD-MCP-Server", report["components"])
        self.assertIn("KiCad + KiBot container", report["components"])
        self.assertIn("Gerbv", report["components"])
        self.assertIn("GitNexus", report["components"])
        self.assertIn("PyGerber", report["components"])
        self.assertIn("QMK container", report["components"])
        self.assertIn("NextPCB HQDFM browser runner", report["components"])
        # A dry-run is an inventory operation, so it must remain useful on a
        # clean machine.  Missing prerequisites are reported truthfully and
        # are enforced only when an installation that needs them is applied.
        for tool in ("kicad-cli", "docker"):
            state = report["prerequisites"][tool]
            self.assertIn(state["status"], {"pass", "fail"})
            self.assertEqual(state["status"], "pass" if state["path"] else "fail")
        self.assertEqual(report["destinations"]["skills"], str((codex_home / "skills").resolve()))
        self.assertEqual(
            report["destinations"]["mcp"],
            str((codex_home / "tools" / "kicad-mcp-server").resolve()),
        )
        self.assertEqual(
            report["destinations"]["dfm_browser"],
            str((codex_home / "tools" / "nextpcb-dfm-browser").resolve()),
        )

    def test_install_copies_validated_skills_without_credentials(self) -> None:
        sentinel = "do-not-copy-this-credential"
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / "codex-home"
            result = self.run_cli_with_env(
                [
                    "install",
                    "--codex-home",
                    str(codex_home),
                    "--skills-only",
                    "--json",
                ],
                {"JLCPCB_API_SECRET": sentinel},
            )

            installed = sorted(path.name for path in (codex_home / "skills").iterdir())
            copied_text = "\n".join(
                path.read_text(errors="ignore")
                for path in (codex_home / "skills").rglob("*")
                if path.is_file()
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            installed,
            ["kicad-design-review", "kicad-pcb-design", "kicad-toolchain-setup"],
        )
        self.assertNotIn(sentinel, copied_text)
        self.assertEqual(json.loads(result.stdout)["result"], "pass")

    def test_install_stages_the_pinned_mcp_without_credentials(self) -> None:
        sentinel = "do-not-stage-this-credential"
        with tempfile.TemporaryDirectory() as temporary:
            codex_home = Path(temporary) / "codex-home"
            result = self.run_cli_with_env(
                [
                    "install",
                    "--codex-home",
                    str(codex_home),
                    "--skip-system-tools",
                    "--skip-mcp-build",
                    "--skip-mcp-registration",
                    "--skip-qmk-setup",
                    "--skip-dfm-browser-build",
                    "--json",
                ],
                {"JLCPCB_API_SECRET": sentinel},
            )

            mcp_target = codex_home / "tools" / "kicad-mcp-server"
            package = json.loads((mcp_target / "package.json").read_text())
            provenance = json.loads((mcp_target / "TOOLKIT-PROVENANCE.json").read_text())
            copied_text = "\n".join(
                path.read_text(errors="ignore")
                for path in codex_home.rglob("*")
                if path.is_file()
            )
            browser_runner_installed = (
                codex_home / "tools" / "nextpcb-dfm-browser" / "nextpcb-dfm.mjs"
            ).is_file()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(package["version"], "2.6.0")
        self.assertEqual(provenance["commit"], "3ab354ca891e905dcc987219845e4a93c2167f85")
        self.assertNotIn(sentinel, copied_text)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "pass")
        self.assertEqual(report["mcp"]["build"], "skipped")
        self.assertEqual(report["mcp"]["registration"], "skipped")
        self.assertTrue(browser_runner_installed)
        self.assertEqual(report["dfm_browser"]["build"], "skipped")

    def test_mcp_smoke_test_negotiates_protocol_and_lists_tools(self) -> None:
        result = self.run_cli("mcp", "test", "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "pass")
        self.assertEqual(report["server"]["name"], "kicad-mcp-server")
        self.assertEqual(report["server"]["version"], "2.6.0")
        self.assertGreaterEqual(report["advertised_tool_count"], 3)
        for tool in ("list_tool_categories", "get_category_tools", "search_tools"):
            self.assertIn(tool, report["advertised_tools"])

    def test_release_rejects_an_incomplete_project(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "Broken.kicad_pro"
            project.write_text("{}")
            result = self.run_cli("release", str(project), "--json")

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "fail")
        self.assertIn("schematic", report["error"])

    def test_dfm_requires_explicit_external_upload_acknowledgement(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "board.zip"
            with __import__("zipfile").ZipFile(archive, "w") as bundle:
                bundle.writestr("board-F_Cu.gbr", "G04 fixture*")
                bundle.writestr("board.drl", "M48\nM30\n")
            result = self.run_cli("dfm", str(archive), "--json")

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "blocked")
        self.assertEqual(report["provider"], "nextpcb")
        self.assertIn("--allow-upload", report["error"])

    def test_dfm_rejects_a_non_zip_upload_before_contacting_provider(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "board.zip"
            archive.write_text("not a zip")
            result = self.run_cli("dfm", str(archive), "--allow-upload", "--json")

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "blocked")
        self.assertIn("valid ZIP", report["error"])

    def test_dfm_rejects_a_zip_without_kicad_or_fabrication_data(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "board.zip"
            with __import__("zipfile").ZipFile(archive, "w") as bundle:
                bundle.writestr("notes.txt", "not board data")
            result = self.run_cli("dfm", str(archive), "--allow-upload", "--json")

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "blocked")
        self.assertIn("Gerber and drill files or a KiCad PCB", report["error"])

    def test_dfm_browserbase_backend_requires_an_inherited_key(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "board.zip"
            with __import__("zipfile").ZipFile(archive, "w") as bundle:
                bundle.writestr("board-F_Cu.gbr", "G04 fixture*")
                bundle.writestr("board.drl", "M48\nM30\n")
            environment = os.environ.copy()
            environment.pop("BROWSERBASE_API_KEY", None)
            result = subprocess.run(
                [
                    str(CLI), "dfm", str(archive), "--allow-upload",
                    "--browser-backend", "browserbase", "--json",
                ],
                cwd=REPO,
                env=environment,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "blocked")
        self.assertIn("BROWSERBASE_API_KEY", report["error"])

    def test_dfm_captures_a_no_findings_external_report_with_source_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "board.zip"
            with __import__("zipfile").ZipFile(archive, "w") as bundle:
                bundle.writestr("board-F_Cu.gbr", "G04 fixture*")
                bundle.writestr("board.drl", "M48\nM30\n")
            runner, tools = self.make_dfm_boundaries(
                root,
                "HQDFM Design for Manufacture(DFM) Report\nSignal Integrity Pass 10\n",
            )
            output = root / "evidence"
            result = self.run_cli_with_env(
                ["dfm", str(archive), "--allow-upload", "--output", str(output), "--json"],
                {
                    "PCB_AGENT_DFM_RUNNER": str(runner),
                    "PCB_AGENT_CHROME": sys.executable,
                    "PATH": f"{tools}{os.pathsep}{os.environ['PATH']}",
                },
            )

            evidence = json.loads((output / "dfm-report.json").read_text())
            sums = (output / "SHA256SUMS").read_text()

        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "pass")
        self.assertEqual(report["verdict"], "no-reported-findings")
        self.assertEqual(report["finding_count"], 0)
        self.assertEqual(evidence["archive_sha256"], report["archive_sha256"])
        self.assertIn("hqdfm-report.pdf", sums)
        self.assertIn("hqdfm-report.txt", sums)

    def test_dfm_fails_closed_when_the_external_report_contains_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "board.zip"
            with __import__("zipfile").ZipFile(archive, "w") as bundle:
                bundle.writestr("board-F_Cu.gbr", "G04 fixture*")
                bundle.writestr("board.drl", "M48\nM30\n")
            runner, tools = self.make_dfm_boundaries(
                root,
                "HQDFM Design for Manufacture(DFM) Report\n"
                "Smallest Trace Spacing Pass 251, Fail 28\nDrill to Copper Pass 35, Fail 93\n",
            )
            output = root / "evidence"
            result = self.run_cli_with_env(
                ["dfm", str(archive), "--allow-upload", "--output", str(output), "--json"],
                {
                    "PCB_AGENT_DFM_RUNNER": str(runner),
                    "PCB_AGENT_CHROME": sys.executable,
                    "PATH": f"{tools}{os.pathsep}{os.environ['PATH']}",
                },
            )

            evidence = json.loads((output / "dfm-report.json").read_text())

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "fail")
        self.assertEqual(report["analysis_status"], "completed")
        self.assertEqual(report["verdict"], "reported-findings")
        self.assertEqual(report["finding_count"], 121)
        self.assertEqual(evidence["finding_count"], 121)

    def test_dfm_fails_closed_on_an_unquantified_reported_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "board.zip"
            with __import__("zipfile").ZipFile(archive, "w") as bundle:
                bundle.writestr("board-F_Cu.gbr", "G04 fixture*")
                bundle.writestr("board.drl", "M48\nM30\n")
            runner, tools = self.make_dfm_boundaries(
                root,
                "HQDFM Design for Manufacture(DFM) Report\nSolder Mask Analysis Fail\n",
            )
            result = self.run_cli_with_env(
                ["dfm", str(archive), "--allow-upload", "--output", str(root / "evidence"), "--json"],
                {
                    "PCB_AGENT_DFM_RUNNER": str(runner),
                    "PCB_AGENT_CHROME": sys.executable,
                    "PATH": f"{tools}{os.pathsep}{os.environ['PATH']}",
                },
            )

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "fail")
        self.assertEqual(report["verdict"], "reported-findings-unquantified")
        self.assertIsNone(report["finding_count"])

    def test_dfm_auto_prefers_an_injected_browserbase_session(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "board.zip"
            with __import__("zipfile").ZipFile(archive, "w") as bundle:
                bundle.writestr("board-F_Cu.gbr", "G04 fixture*")
                bundle.writestr("board.drl", "M48\nM30\n")
            runner, tools = self.make_dfm_boundaries(
                root,
                "HQDFM Design for Manufacture(DFM) Report\nSignal Integrity Pass 10\n",
            )
            result = self.run_cli_with_env(
                ["dfm", str(archive), "--allow-upload", "--output", str(root / "evidence"), "--json"],
                {
                    "BROWSERBASE_API_KEY": "injected-fixture-key",
                    "PCB_AGENT_DFM_RUNNER": str(runner),
                    "PATH": f"{tools}{os.pathsep}{os.environ['PATH']}",
                },
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["browser_backend"], "browserbase")
        self.assertEqual(report["browser_session_id"], "fixture-session")
        self.assertEqual(report["browserbase_download"]["cloud_cleanup"], "pass")
        self.assertNotIn("injected-fixture-key", result.stdout)

    def test_dfm_blocks_if_the_archive_changes_during_upload(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "board.zip"
            with __import__("zipfile").ZipFile(archive, "w") as bundle:
                bundle.writestr("board-F_Cu.gbr", "G04 fixture*")
                bundle.writestr("board.drl", "M48\nM30\n")
            runner, tools = self.make_dfm_boundaries(
                root,
                "HQDFM Design for Manufacture(DFM) Report\nSignal Integrity Pass 10\n",
            )
            result = self.run_cli_with_env(
                ["dfm", str(archive), "--allow-upload", "--output", str(root / "evidence"), "--json"],
                {
                    "PCB_AGENT_CHROME": sys.executable,
                    "PCB_AGENT_DFM_RUNNER": str(runner),
                    "PCB_AGENT_TEST_MUTATE_ARCHIVE": "1",
                    "PATH": f"{tools}{os.pathsep}{os.environ['PATH']}",
                },
            )

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "blocked")
        self.assertIn("changed during external DFM", report["error"])

    def test_dfm_blocks_a_browserbase_download_checksum_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "board.zip"
            with __import__("zipfile").ZipFile(archive, "w") as bundle:
                bundle.writestr("board-F_Cu.gbr", "G04 fixture*")
                bundle.writestr("board.drl", "M48\nM30\n")
            runner, tools = self.make_dfm_boundaries(
                root,
                "HQDFM Design for Manufacture(DFM) Report\nSignal Integrity Pass 10\n",
            )
            result = self.run_cli_with_env(
                ["dfm", str(archive), "--allow-upload", "--output", str(root / "evidence"), "--json"],
                {
                    "BROWSERBASE_API_KEY": "injected-fixture-key",
                    "PCB_AGENT_DFM_RUNNER": str(runner),
                    "PCB_AGENT_TEST_BAD_DOWNLOAD_HASH": "1",
                    "PATH": f"{tools}{os.pathsep}{os.environ['PATH']}",
                },
            )

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "blocked")
        self.assertIn("checksum does not match", report["error"])

    def test_release_generates_and_independently_parses_fabrication_outputs(self) -> None:
        fixture = REPO / "examples" / "tenkey-macropad" / "source"
        with tempfile.TemporaryDirectory() as temporary:
            project_dir = Path(temporary) / "project"
            shutil.copytree(
                fixture,
                project_dir,
                ignore=shutil.ignore_patterns("outputs", "*.kicad_prl", "*.lck"),
            )
            project = project_dir / "TenKeyMacroPad.kicad_pro"
            before = {
                path.relative_to(project_dir): path.read_bytes()
                for path in project_dir.rglob("*")
                if path.is_file()
            }
            output = Path(temporary) / "release"
            result = self.run_cli(
                "release",
                str(project),
                "--output",
                str(output),
                "--skip-container",
                "--json",
            )
            archive_names = []
            with __import__("zipfile").ZipFile(output / "fabrication" / "TenKeyMacroPad-JLCPCB.zip") as archive:
                archive_names = archive.namelist()

            report_file = json.loads((output / "release-report.json").read_text())
            manifest = (output / "SHA256SUMS").read_text()
            after = {
                path.relative_to(project_dir): path.read_bytes()
                for path in project_dir.rglob("*")
                if path.is_file()
            }

        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "pass")
        self.assertEqual(report_file["checks"]["erc"], "pass")
        self.assertEqual(report_file["checks"]["drc"], "pass")
        self.assertEqual(report_file["checks"]["gerbv"], "pass")
        self.assertEqual(report_file["checks"]["pygerber"], "pass")
        self.assertEqual(report_file["checks"]["source_unchanged"], "pass")
        self.assertGreaterEqual(len([name for name in archive_names if name.endswith(".gbr")]), 9)
        self.assertGreaterEqual(len([name for name in archive_names if name.endswith(".drl")]), 2)
        self.assertIn("TenKeyMacroPad-JLCPCB.zip", manifest)
        self.assertEqual(after, before)

    def test_example_qmk_matrix_matches_the_documented_hardware_contract(self) -> None:
        example = REPO / "examples" / "tenkey-macropad"
        contract = json.loads((example / "design" / "pin-firmware-contract.json").read_text())
        keyboard = json.loads(
            (example / "source" / "firmware" / "qmk" / "tenkey_macropad" / "keyboard.json").read_text()
        )

        self.assertEqual(keyboard["diode_direction"], contract["matrix"]["diode_direction"])
        self.assertEqual(
            keyboard["matrix_pins"]["rows"],
            [row["avr_port"] for row in contract["matrix"]["rows"]],
        )
        self.assertEqual(
            keyboard["matrix_pins"]["cols"],
            [column["avr_port"] for column in contract["matrix"]["columns"]],
        )
        self.assertEqual(keyboard["usb"]["max_power"], contract["usb"]["max_power_descriptor_mA"])


if __name__ == "__main__":
    unittest.main()
