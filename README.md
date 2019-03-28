# IndorHome
This Python script monitors your local network and notifies you of known hosts.

The network scan occurs every 60 seconds and the program is required to run as root to capture MAC-addresses of the network devices.

## Installation
Python modules
```bash
pip install --no-cache-dir -r requirements.txt
```

Discover hosts on your local network
```bash
sudo nmap -sn 192.168.1.0/24
```

#### Setup the config file
```bash
touch config.json
vim config.json
```

```json
{
  "hosts": {
    "Example 1": ["00:00:00:00:00:00"],
    "Example 2": ["00:00:00:00:00:00"]
  }
}
```

If you wish to run the script on system start you can use the prodvided init.d script (Linux only). Make sure you modify the init.d script to fit your needs (correct user and paths).
```bash
chmod +x initd.sh
sudo cp initd.sh /etc/init.d/collector
touch /var/log/collector.log && chown root /var/log/collector.log # CHANGE USER HERE
update-rc.d collector defaults
service \"collector\" start"
```

#### Execution
Make sure to run the program as root in order to collect MAC addresses from the network interface.
```bash
sudo python collector.py
```


#### Requirements
Make sure you have the following programms installed and running on your system:

Python (only tested version 2.7)
NMap
