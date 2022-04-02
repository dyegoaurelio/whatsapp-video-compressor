SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

fileDir=$SCRIPT_DIR/__main__.py

execPath=~/.local/bin/whatsapp-compressor

ln -sf $fileDir $execPath

chmod +x $fileDir
chmod +x $execPath