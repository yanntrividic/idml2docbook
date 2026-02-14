import subprocess
import sys
import re
import shutil
import os
from packaging import version
from pathlib import Path
from dotenv import load_dotenv

REPO_URL = "https://github.com/yanntrividic/idml2xml-frontend.git"
REPO_NAME = "idml2xml-frontend"

ENV_SAMPLE = """
# Path to Transpect's idml2xml-frontend, cloned from:
# https://github.com/yanntrividic/idml2xml-frontend
IDML2HUBXML_SCRIPT_FOLDER="/path/to/idml2xml-frontend"

# Command or path to the right bash executable (>= 5.0.0)
BASH="bash"

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

def check_java(verbose=False):
    """Returns the Java version
    Based on https://www.getorchestra.io/guides/how-to-check-java-version-in-python-with-apache-iceberg
    """
    try:
        result = subprocess.run(['java', '-version'], stderr=subprocess.PIPE, text=True)
        output = result.stderr

        if 'version' not in output:
            if verbose:
                print("❌ Java version could not be determined.")
            return -1

        version_line = output.splitlines()[0]
        java_version = version_line.split('"')[1]

        match = re.match(r'(\d+)(?:\.(\d+))?', java_version)
        if not match:
            if verbose: print("❌ Could not parse Java version.")
            return -1

        major = int(match.group(1))

        # Handle old scheme: 1.x -> x is real major
        if major == 1 and match.group(2):
            major = int(match.group(2))

        if major >= 7:
            if verbose: print(f"✅ Java major version is {major} (>= 7)")
            return major
        else:
            if verbose: print(f"❌ Java version {major} is lower than required (>= 7).")
            return -1

    except FileNotFoundError:
        if verbose: print("❌ Java is not installed or not in the system PATH.")
        return -1

def check_git(verbose=True):
    if not shutil.which("git"):
        sys.exit("❌ Git not found. Please install git to install idml2xml-frontend")
        return -1
    return 1

def check_bash(verbose=False):
    """Returns the bash version
    """
    try:
        # Run the 'java -version' command
        result = subprocess.run([os.getenv("BASH"), '--version'], stdout=subprocess.PIPE, text=True)
        # Java version information is in the stderr output
        output = result.stdout
        # Extract the version number
        if 'version' in output:
            bash_version = output.splitlines()[0]
            # Extract the semantic versioning number using regex
            match = re.search(r'\d+\.\d+\.\d+', bash_version)
            if match:
                semver = match.group(0)
                # Compare with 7.0.0 using packaging.version
                if version.parse(semver) >= version.parse("5.0.0"):
                    if(verbose): print(f"✅ Bash version is {semver} (>= 5.0.0)")
                    return semver
                else:
                    if(verbose): print(f"❌ Bash version {semver} is lower than required (>= 5.0.0).\nPlease install a more recent version or specify the path to the right executable in your .env file.")
                    return -1
            else:
                if(verbose): print("❌ Could not extract a valid semantic version number from Bash version string.")
                return -1
        else:
            if(verbose): print("❌ Bash version could not be determined.")
            return -1
    except FileNotFoundError:
        if(verbose): print("❌ Bash is not installed or not in the system PATH.")
        return -1


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
        "IDML2HUBXML_SCRIPT_FOLDER.")
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

    verbose = True
    check_git(verbose)

    target = Path(input(f"📝 Clone {REPO_NAME} into directory [.]? Else type your path: ") or ".").expanduser().resolve()
    repo_dir = clone_repo(target)

    configure_env(target, repo_dir)
    load_dotenv()

    check_bash(verbose)
    check_java(verbose)

    print("🎉 Environment configured!")

if __name__ == "__main__":
    main()