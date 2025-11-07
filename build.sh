#!/usr/bin/env bash
set -o errexit

STORAGE_DIR=/opt/render/project/.render

echo "=== Installing Google Chrome ==="
if [[ ! -d $STORAGE_DIR/chrome ]]; then
  mkdir -p $STORAGE_DIR/chrome
  cd $STORAGE_DIR/chrome
  wget -P ./ https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -x ./google-chrome-stable_current_amd64.deb $STORAGE_DIR/chrome
  rm ./google-chrome-stable_current_amd64.deb
else
  echo "...Using cached Chrome"
fi
export PATH="${PATH}:$STORAGE_DIR/chrome/opt/google/chrome"

echo "=== Installing ChromeDriver ==="
LATEST=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json | grep -m1 -A4 "linux64" | grep "url" | head -1 | cut -d '"' -f 4)
wget -q "$LATEST" -O chromedriver.zip
unzip -o chromedriver.zip
mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver
rm -rf chromedriver* LICENSE.chromedriver

echo "=== Installing Python packages ==="
pip install -r requirements.txt
