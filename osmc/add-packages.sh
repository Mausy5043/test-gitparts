# Stop XBMC to allow tinkering
echo "Stopping KODI ..."
sudo systemctl stop mediacenter

#killem=$(ps aux|pgrep kodi)
#echo "kodi PID = "$killem

echo "Installing packages..."
sudo apt-get update
sudo apt-get -yuV install bc rsync htop screen git cron wavemon
