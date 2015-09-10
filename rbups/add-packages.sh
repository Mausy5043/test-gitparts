echo "Installing UPS monitor packages..."
sudo apt-get -yuV install nut-client nut-server

echo "Installing CUPS packages..."
sudo apt-get -yuV install cups cifs-utils
echo "Pausing... (1/4) "
sleep 60
sudo apt-get -yuV install hplip-cups openprinting-ppds
echo "Pausing... (2/4) "
sleep 60
sudo apt-get -yuV install cups-pdf cups-driver-gutenprint
echo "Pausing... (3/4) "
sleep 60
sudo apt-get -yuV install python-cups python-daemon python-pkg-resources
sudo apt-get -yuV install python-mysqldb
echo "Pausing... (4/4)"
sleep 60
