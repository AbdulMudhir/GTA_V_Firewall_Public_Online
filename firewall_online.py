import subprocess
import os
import ctypes

firewall_rule_name = "GTA Online Firewall Rule"
program_path = "C:\GTAV\GTA5.exe"


def running_as_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def firewall_exist():
    pass


def add_firewall_rule():
    netsh_add_firewall_command = f'''netsh advfirewall firewall add rule name="{firewall_rule_name}" dir=in action=block program="{program_path}" enable=no profile=domain,private,public protocol=UDP localport=6672'''
    subprocess.call(netsh_add_firewall_command)


def add_white_list(ip_address):
    netsh_allow_remote_address = f'''netsh advfirewall firewall set rule name="{firewall_rule_name}" new remoteip={ip_address}'''
    subprocess.call(netsh_allow_remote_address)

def enable_firewall_rule():
    netsh_add_firewall_command = f'''netsh advfirewall firewall set rule name="{firewall_rule_name}" enable=yes '''
    subprocess.call(netsh_add_firewall_command)



def delete_firewall_rule():
    netsh_add_firewall_command = f'''netsh advfirewall firewall delete rule name="{firewall_rule_name}" '''
    subprocess.call(netsh_add_firewall_command)

delete_firewall_rule()

def enable_firewall_rule(firewall_rule_name):
    pass
