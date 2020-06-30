import configparser
import time
startTime = time.time()
import ipaddress
import os.path
import random
from pyfiglet import Figlet
from colorama import  Fore
from scapy.all import *


red=Fore.RED
green=Fore.GREEN
yel=Fore.YELLOW
reset=Fore.RESET ; print(reset)

logo = Figlet(font='graffiti')
print(green+logo.renderText('\n%R##########Remoterz.net#########%R'+reset))
conf = configparser.ConfigParser()

def config():
    global all_ip
    global ports
    global countip
    global countport
    global  startTime
    startTime = time.time()
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
        print('config was created'+reset)
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
        if res is None:
            print(f"{red}+{all_ip[i]} -----> Host is down'{reset}")
        else:
            print(f"{green}+{all_ip[i]} -----> Host is up{reset}")
            for j in range(countport):
                srcport=random.randint(1025, 60000)
                ip = str(all_ip[i])
                tcp = sr1(IP(dst=ip) / TCP(sport=srcport,dport=ports[j], flags="S"), timeout=1, verbose=0 )

                if tcp is not  None :
                    flag = tcp.getlayer(TCP).flags
                    if flag ==  "SA": #or 0x12
                        sr1(IP(dst=ip) / TCP(sport=srcport,dport=ports[j], flags='R'), timeout=1, verbose=0, )
                        print(f"   {green} {ip}:{ports[j]} is listening.  {reset}")

                    if  flag == "RA": #or 0x14
                        print(f"{red}    {ip}:{ports[j]} is close.  {reset}")
                if tcp is None:
                        print(f"{yel}    {ip}:{ports[j]} is {red}filtered {yel}(silently dropped).{reset}")

    print(f'The script took {(time.time() - startTime)} second !')
config()
checkhost()
