from pathlib import Path
import json
import os
import shutil
import subprocess
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

    def test_help_exposes_the_confirmed_pipeline(self) -> None:
        result = self.run_cli("--help")

        self.assertEqual(result.returncode, 0, result.stderr)
        for command in ("install", "doctor", "validate", "mcp", "release"):
            self.assertIn(command, result.stdout)

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
        for tool in (
            "codex",
            "docker",
            "gerbv",
            "gitnexus",
            "kicad-cli",
            "node",
            "npm",
            "pygerber",
            "python3",
        ):
            self.assertEqual(report["tools"][tool]["status"], "pass", tool)
        self.assertEqual(report["mcp"]["build"], "pass")
        self.assertEqual(report["mcp"]["codex_registration"], "pass")

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
        self.assertEqual(report["prerequisites"]["kicad-cli"]["status"], "pass")
        self.assertEqual(report["prerequisites"]["docker"]["status"], "pass")
        self.assertEqual(report["destinations"]["skills"], str((codex_home / "skills").resolve()))
        self.assertEqual(
            report["destinations"]["mcp"],
            str((codex_home / "tools" / "kicad-mcp-server").resolve()),
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

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(package["version"], "2.6.0")
        self.assertEqual(provenance["commit"], "3ab354ca891e905dcc987219845e4a93c2167f85")
        self.assertNotIn(sentinel, copied_text)
        report = json.loads(result.stdout)
        self.assertEqual(report["result"], "pass")
        self.assertEqual(report["mcp"]["build"], "skipped")
        self.assertEqual(report["mcp"]["registration"], "skipped")

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
