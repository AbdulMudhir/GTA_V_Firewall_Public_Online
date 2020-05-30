from subprocess import call, check_output, check_call, Popen, PIPE
import os
import ctypes

firewall_rule_name = "GTA Online Firewall Rule"
program_path = "C:\GTAV\GTA5.exe"


def running_as_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def firewall_exist():
    netsh_firewall_exist = f'''netsh advfirewall firewall show rule name="{firewall_rule_name}"'''
    in_command = Popen(netsh_firewall_exist, stdout=PIPE, stderr=PIPE)

    output_message, _ = in_command.communicate()

    return "No rules match the specified criteria." == output_message.decode().strip()


def firewall_scopes_list():

    if firewall_exist():

        netsh_firewall_exist = f'''netsh advfirewall firewall show rule name="{firewall_rule_name}"'''
        in_command = Popen(netsh_firewall_exist, stdout=PIPE, stderr=PIPE)

        output_message, _ = in_command.communicate()




def add_firewall_rule():
    netsh_add_firewall_command_in = f'''netsh advfirewall firewall add rule name="{firewall_rule_name}" dir=in action=block program="{program_path}" enable=no profile=domain,private,public protocol=UDP localport=6672  '''
    netsh_add_firewall_command_out = f'''netsh advfirewall firewall add rule name="{firewall_rule_name}" dir=out action=block program="{program_path}" enable=no profile=domain,private,public protocol=UDP localport=6672'''
    in_command = Popen(netsh_add_firewall_command_in, stdout=PIPE, stderr=PIPE)
    out_command = Popen(netsh_add_firewall_command_out, stdout=PIPE, stderr=PIPE)

    output_message, _ = in_command.communicate()

    return "Ok." == output_message.decode().strip()




def add_white_list(ip_address):
    netsh_allow_remote_address = f'''netsh advfirewall firewall set rule name="{firewall_rule_name}" dir=in new remoteip={ip_address} '''
    call(netsh_allow_remote_address)


def enable_firewall_rule():
    netsh_add_firewall_command = f'''netsh advfirewall firewall set rule name="{firewall_rule_name}" enable=yes '''
    call(netsh_add_firewall_command)


def disabl_firewall_rule():
    netsh_add_firewall_command = f'''netsh advfirewall firewall set rule name="{firewall_rule_name}" enable=no '''
    call(netsh_add_firewall_command)


def delete_firewall_rule():
    netsh_add_firewall_command = f'''netsh advfirewall firewall delete rule name="{firewall_rule_name}" '''
    call(netsh_add_firewall_command)


delete_firewall_rule()
add_firewall_rule()
add_white_list("192.168.1.1")