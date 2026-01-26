import subprocess
import sys
import shutil
import os
from pathlib import Path

REPO_URL = "https://github.com/transpect/idml2xml-frontend.git"
REPO_NAME = "idml2xml-frontend"

ENV_SAMPLE = """
# Path to Transpect's idml2xml-frontend, clone from:
# https://github.com/transpect/idml2xml
IDML2HUBXML_SCRIPT_FOLDER="/path/to/idml2xml-frontend"

# This folder will get created
IDML2HUBXML_OUTPUT_FOLDER="idml2hubxml"

# Override defaults values by uncommenting/editing these lines:
# IGNORE_OVERRIDES=True
# TYPOGRAPHY=True
# THIN_SPACES=True
# LINEBREAKS=True
# MEDIA="images"
# RASTER="jpg"
# VECTOR="svg"
"""


def run(cmd):
    print(">", " ".join(cmd))
    subprocess.check_call(cmd)

def check_java():
    try:
        out = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT)
        print("✅ Java found:", out.decode().splitlines()[0])
    except Exception:
        sys.exit("❌ Java not found. Please install Java >= 7")

def check_git():
    if not shutil.which("git"):
        sys.exit("❌ Git not found. Please install git")

def clone_repo(target_dir: Path):
    repo_dir = target_dir / REPO_NAME
    if repo_dir.exists():
        print(f"✅ {repo_dir} already exists")
        return repo_dir
    run(["git", "clone", "--recurse-submodules", REPO_URL, str(repo_dir)])
    return repo_dir

def configure_env(target_dir: Path, repo_dir: Path):
    if Path(".env").exists():
        print("⚠️ .env already exists. Please make sure it already contains values for",
        "IDML2HUBXML_SCRIPT_FOLDER and IDML2HUBXML_OUTPUT_FOLDER.")
        return

    content = ENV_SAMPLE.replace(
        f'IDML2HUBXML_SCRIPT_FOLDER="/path/to/idml2xml-frontend"',
        f'IDML2HUBXML_SCRIPT_FOLDER="{repo_dir}"'
    )
    content = content.replace(
        f'IDML2HUBXML_OUTPUT_FOLDER="idml2hubxml"',
        f'IDML2HUBXML_OUTPUT_FOLDER="{target_dir}/idml2hubxml"'
    )
    Path(".env").write_text(content)

    print("✅ .env configured")

def main():
    print("⏳ Installing external dependencies for idml2docbook")

    check_java()
    check_git()

    target = Path(input("📝 Clone repo into directory [.]? ") or ".").expanduser().resolve()
    repo_dir = clone_repo(target)

    configure_env(target, repo_dir)

    print("🎉 Environment configured!")

if __name__ == "__main__":
    main()