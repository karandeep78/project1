"""Render entrypoint wrapper for nested Flask project."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parent / "Phishing-detector"
APP_FILE = PROJECT_DIR / "app.py"

# Make nested project imports (convert, feature, etc.) resolvable.
sys.path.insert(0, str(PROJECT_DIR))

spec = spec_from_file_location("phishing_detector_app", APP_FILE)
module = module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

app = module.app
