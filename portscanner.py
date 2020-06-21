import configparser
import ipaddress
import os.path

from pyfiglet import Figlet
from scapy.all import *

logo = Figlet(font='bubble')
print(logo.renderText("Remoterz.net"))
conf = configparser.ConfigParser()


def config():
    global all_ip
    global ports
    global countip
    global countport
    if os.path.exists('config.cfg'):
        print('##config.cfg is exist##')
    else:
        conf.add_section('hosts')
        conf.set('hosts', 'range', '192.168.10.0/24')
        conf.add_section('port')
        conf.set('port', 'start_end', '22,22')
        with open('config.cfg', 'w') as configfile:
            conf.write(configfile)
        configfile.close()
        print('config was created please edit configuration and try again !')
        exit(1)
    ##read config to list
    conf.read('config.cfg')
    ip_addr = conf.get('hosts', 'range')
    port = conf.get('port', 'start_end').split(',')
    min_port = int(port[0])
    max_port = int(port[1])
    # list_ip
    all_ip = []
    countip = 0
    for ip_addr in ipaddress.IPv4Network(ip_addr):
        countip += 1
        all_ip.append(ip_addr)
    # list_port
    ports = []
    countport = 0
    # ok
    for i in range(min_port, max_port + 1):
        countport += 1
        ports.append(i)
    if countport == 0:
        countport = 1


def checkhost():
    for i in range(countip):
        ping = IP(dst=str(all_ip[i])) / ICMP()
        res = sr1(ping, timeout=1, verbose=0)
        if res == None:
            print(all_ip[i], 'is down')
        else:
            print(all_ip[i], '>>>>>>>>>>is up')
            for j in range(countport):
                tcp_request = IP(dst=all_ip[i]) / TCP(dport=ports[j], flags="S")
                tcp_response = sr1(tcp_request, timeout=1, verbose=0)
                try:
                    if tcp_response.getlayer(TCP).flags == "SA":
                        new=(port, "***is listening")
                    print(new)
                except AttributeError:
                    print(ports[j], "---is not listening")

config()
checkhost()
