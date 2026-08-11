#!/usr/bin/env python3
"""Compatibility entry point for the repository validation contract."""

from pathlib import Path
import os
import sys


ROOT = Path(__file__).resolve().parents[1]
os.execv(str(ROOT / "pcb-agent"), [str(ROOT / "pcb-agent"), "validate", *sys.argv[1:]])
