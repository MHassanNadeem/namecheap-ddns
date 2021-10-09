# namecheap-ddns

namecheap ddns provider module for python/synology NAS

## Prerequisites

```bash
sudo python3 -m ensurepip
sudo python3 -m pip install --upgrade pip
pip3 install requests
```

## Installation on Synology NAS

```bash
sudo -i

# Copy the code and set permissions
cp ./namecheap_ddns.py /usr/local/bin/namecheap_ddns.py
chmod a+x /usr/local/bin/namecheap_ddns.py

# Add provider
cat >> /etc.defaults/ddns_provider.conf << 'EOF'
[Namecheap]
        modulepath=/usr/local/bin/namecheap_ddns.sh
        queryurl=https://dynamicdns.park-your-domain.com/update
        website=https://namecheap.com
EOF
```