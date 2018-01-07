Steps to automate service on boot for sysjourney code: 

1) move the file 'sysjourney.service' to the directory '/lib/systemd/system/'

2) Execute command: sudo chmod 644 /lib/systemd/system/sysjourney.service

3) Execute command:  sudo systemctl daemon-reload

4) Execute command: sudo systemctl enable sysjourney.service