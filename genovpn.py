#!/usr/bin/python
import httplib
import string
import random
import os

url = "http://members.3322.org/dyndns/getip"
conn = httplib.HTTPConnection("members.3322.org")
conn.request(method="GET",url=url)
response = conn.getresponse()
public_ip = response.read().replace("\n", "", -1)

tpl = open('vpn.ovpn', 'r').read()
ca = open('/etc/openvpn/keys/ca.crt', 'r').read()
client_crt = open('/etc/openvpn/keys/client1.crt', 'r').read()
nStart = client_crt.index("-----BEGIN CERTIFICATE-----")
client_crt = client_crt[nStart:]
client_key = open('/etc/openvpn/keys/client1.key', 'r').read()

ca = ca[:-1]
client_crt = client_crt[:-1]
client_key = client_key[:-1]

tpl = tpl.replace("{{public-ip}}", public_ip, -1)
tpl = tpl.replace("{{ca-crt}}", ca, -1)
tpl = tpl.replace("{{client-crt}}", client_crt, -1)
tpl = tpl.replace("{{client-key}}", client_key, -1)

strRand = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
dir = "/var/www/html/" + strRand
if not os.path.exists(dir):
    os.makedirs(dir)

with open(dir + "/vpn.ovpn", "w") as file:
        file.write(tpl)
print "http://" + public_ip + ":<pubblic_port>/" + strRand