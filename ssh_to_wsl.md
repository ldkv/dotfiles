<!-- https://medium.com/@wuzhenquan/windows-and-wsl-2-setup-for-ssh-remote-access-013955b2f421 -->

In WSL2:

```bash
sudo apt remove openssh-server
sudo apt install openssh-server
sudo vi /etc/ssh/sshd_config, enable Port 22 and PasswordAuthentication yes
sudo service ssh restart
```

Open Powershell in administrator mode.

Port forwarding:

```shell
netsh interface portproxy add v4tov4 `
  listenaddress=192.168.1.12 `
  listenport=2222 `
  connectaddress=172.18.95.67 `
  connectport=22
```

`listenaddress` is the IP address of the Windows host, `connectaddress` is the IP address of the WSL2 VM.

Add firewall rule:

```shell
netsh advfirewall firewall add rule `
name = "Allow Inbound 2222 WSL2 ssh" `
dir=in `
protocol=TCP `
localport=2222 `
action=allow
```

Finally:

```bash
ssh ldkv@192.168.1.12 -p 2222
```
