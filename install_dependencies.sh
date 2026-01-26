#!/bin/bash

###############################################################################
# install.sh – Installation script for the external dependencies of idml2docbook
#
# This script performs a full environment check and setup for the idml2docbook
# toolchain. It ensures all external dependencies are installed, clones
# the necessary hubxml2idml-frontend repository and prepares a .env configuration.
#
# Functionality:
# - Verifies Java (>= 7.0.0) is installed
# - Verifies Git is installed
# - Prompts for a target directory to clone the `idml2xml-frontend` repo
# - Clones idml2xml-frontend and its submodules (if not already present)
# - Copies `.env.sample` to `.env` if needed, and sets correct idml2xml-frontend path
#
# Prerequisites:
# - Bash shell
# - Java >= 7.0.0
# - Git
#
# Usage:
#   chmod +x install.sh
#   ./install.sh
#
# Author: Yann Trividic
# Repository: https://gitlab.com/deborderbollore/idml-pandoc-reader
###############################################################################

version_greater_equal() {
  [ "$(printf '%s\n' "$1" "$2" | sort -V | head -n1)" = "$1" ]
}

echo "Checking Java version..."
if command -v java >/dev/null 2>&1; then
  JAVA_VERSION=$(java -version 2>&1 | awk -F '"' '/version/ {print $2}')
  echo "Java version: $JAVA_VERSION"
  if version_greater_equal "7.0.0" "$JAVA_VERSION"; then
    echo "✅ Java version is sufficient."
  else
    echo "❌ Java version must be >= 7.0.0"
    exit 1
  fi
else
  echo "❌ Java is not installed. Please install Java (>=7.0.0)"
  exit 1
fi

echo "Checking Git installation..."
if command -v git >/dev/null 2>&1; then
  echo "✅ Git is installed: $(git --version)"
else
  echo "❌ Git is not installed. Please install git"
  exit 1
fi

DEFAULT_DIR="$(pwd)"
read -p "Enter directory to clone the repo into [${DEFAULT_DIR}] (the presence of \
pre-existing installations will be checked before installing): " CLONE_DIR
CLONE_DIR="${CLONE_DIR:-$DEFAULT_DIR}"

REPO_NAME="idml2xml-frontend"
IDML2XML_FRONTEND_TARGET_DIR="${CLONE_DIR}/${REPO_NAME}"
EXPECTED_URL="https://github.com/transpect/idml2xml-frontend.git"

if [ -d "$IDML2XML_FRONTEND_TARGET_DIR/.git" ]; then
  ACTUAL_URL=$(git -C "$IDML2XML_FRONTEND_TARGET_DIR" remote get-url origin)
  if [ "$ACTUAL_URL" = "$EXPECTED_URL" ]; then
    echo "✅ Repository already exists at $IDML2XML_FRONTEND_TARGET_DIR and is correct."
  else
    echo "⚠️ Found a Git repo at $IDML2XML_FRONTEND_TARGET_DIR, but remote URL does not match."
    echo "Expected: $EXPECTED_URL"
    echo "Found:    $ACTUAL_URL"
    exit 1
  fi
else
  echo "📦 Cloning $REPO_NAME and submodules into $IDML2XML_FRONTEND_TARGET_DIR..."
  git clone "$EXPECTED_URL" "$IDML2XML_FRONTEND_TARGET_DIR" --recurse-submodules \
    || { echo "❌ Git clone failed."; exit 1; }
fi

if [ -f ".env" ]; then
  echo "✅ .env file already exists. Skipping creation."
else
  if [ ! -f ".env.sample" ]; then
    echo "❌ .env.sample not found. Cannot create .env."
    exit 1
  fi

  echo "📝 Creating .env file from .env.sample..."
  cp .env.sample .env

  ESCAPED_PATH=$(printf '%s\n' "$IDML2XML_FRONTEND_TARGET_DIR" | sed 's:/:\\/:g')
  sed -i '.bak' "s|^IDML2HUBXML_SCRIPT_FOLDER=.*$|IDML2HUBXML_SCRIPT_FOLDER=\"$ESCAPED_PATH\"|" .env

  echo "✅ .env file created and updated with install path of idml2xml-frontend."
  echo "📍 IDML2HUBXML_SCRIPT_FOLDER=$IDML2XML_FRONTEND_TARGET_DIR"
fi