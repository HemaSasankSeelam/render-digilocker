#!/usr/bin/env bash
set -o errexit

STORAGE_DIR=/opt/render/project/.render

# === 1. Install Chrome (cached) ===
if [[ ! -d $STORAGE_DIR/chrome ]]; then
  echo "...Downloading Chrome"
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
else
  echo "...Using cached Chrome"
fi

export PATH="${PATH}:$STORAGE_DIR/chrome/opt/google/chrome"

# === 2. Install matching ChromeDriver ===
CHROME_VERSION=$($STORAGE_DIR/chrome/opt/google/chrome/google-chrome --version | grep -oE "[0-9]+\.[0-9]+\.[0-9]+")
echo "Detected Chrome version: $CHROME_VERSION"
CHROMEDRIVER_VERSION=$(curl -s "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_$CHROME_VERSION")
wget -q "https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip"
unzip chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver
rm -rf chromedriver-linux64*

# === 3. Install Python deps ===
pip install -r requirements.txt
