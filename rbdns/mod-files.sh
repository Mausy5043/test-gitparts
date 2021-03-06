echo "Modifying installation..."

echo -n "Modify /boot/config.txt "
# Scaled CPU frequency
echo ""                         | sudo tee -a /boot/config.txt
echo "# Added by raspboot"      | sudo tee -a /boot/config.txt
echo "arm_freq=950"             | sudo tee -a /boot/config.txt
echo "core_freq=450"            | sudo tee -a /boot/config.txt
echo "sdram_freq=450"           | sudo tee -a /boot/config.txt
echo "over_voltage=6"           | sudo tee -a /boot/config.txt
echo ""                         | sudo tee -a /boot/config.txt
echo "arm_freq_min=500"         | sudo tee -a /boot/config.txt
echo "core_freq_min=250"        | sudo tee -a /boot/config.txt
echo "sdram_freq_min=400"       | sudo tee -a /boot/config.txt
echo "over_voltage_min=0"       | sudo tee -a /boot/config.txt
echo ""                         | sudo tee -a /boot/config.txt
echo "force_turbo=0"            | sudo tee -a /boot/config.txt
echo "temp_limit=70"            | sudo tee -a /boot/config.txt

echo "[OK]"

echo "Modify DNSMASQ installation"
sudo sed -i 's/^#conf-dir=\/etc\/dnsmasq.d$/conf-dir=\/etc\/dnsmasq.d/' /etc/dnsmasq.conf
#sudo sed -i 's/^iface wlan0 inet dhcp/iface wlan0 inet 192\.168\.178\.6/' /etc/network/interfaces
#sudo sed -i 's/^iface eth0 inet dhcp/iface eth0 inet 192\.168\.178\.3/' /etc/network/interfaces
