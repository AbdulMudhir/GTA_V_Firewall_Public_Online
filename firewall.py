from subprocess import call, Popen, PIPE
import re
import ctypes

firewall_rule_name = "GTA Online Firewall Rule"


def running_as_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()


def firewall_exist():
    netsh_firewall_exist = f'''netsh advfirewall firewall show rule name="{firewall_rule_name}"'''
    in_command = Popen(netsh_firewall_exist, stdout=PIPE, stderr=PIPE)

    output_message, _ = in_command.communicate()

    return "No rules match the specified criteria." != output_message.decode().strip()


def firewall_scopes_list():
    if firewall_exist():
        netsh_firewall_exist = f'''netsh advfirewall firewall show rule name="{firewall_rule_name}" dir=in '''
        in_command = Popen(netsh_firewall_exist, stdout=PIPE, stderr=PIPE)

        output_message, _ = in_command.communicate()

        output_message_decoded = output_message.decode().strip()

        remote_ip_address = output_message_decoded.split()[17]

        return remote_ip_address


def valid_ip_address(ip_address):
    ip_address_pattern = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/?\d?\d?"
    check_ip = re.match(ip_address_pattern, ip_address)

    return check_ip is not None


def add_firewall_rule(program_path):
    netsh_add_firewall_command_in = f'''netsh advfirewall firewall add rule name="{firewall_rule_name}" dir=in action=block program="{program_path}" enable=no profile=domain,private,public protocol=UDP localport=6672'''
    netsh_add_firewall_command_out = f'''netsh advfirewall firewall add rule name="{firewall_rule_name}" dir=out action=block program="{program_path}" enable=no profile=domain,private,public protocol=UDP localport=6672'''
    in_command = Popen(netsh_add_firewall_command_in, stdout=PIPE, stderr=PIPE)
    out_command = Popen(netsh_add_firewall_command_out, stdout=PIPE, stderr=PIPE)

    output_message, _ = in_command.communicate()

    return "Ok." == output_message.decode().strip()


def ip_address_scope_addition(scope, ip_address):
    split_scope = scope.split(",")

    split_ip_address = ip_address.split('.')
    # splitting the ip address so we can get a +1 and -1 range of the current ip address
    first_ip = f"{'.'.join(split_ip_address[0:3])}.{int(split_ip_address[-1])-1}"
    second_ip = f"{'.'.join(split_ip_address[0:3])}.{int(split_ip_address[-1]) + 1}"

    print(first_ip, second_ip)

    #
    # for index, i in enumerate(split_scope):
    #     ip_address_split = i.split("-")
    #
    #     print(ip_address_split)
    #
    #     first_octet = int(ip_address_split[0].split('.')[0])
    #     second_octet = int(ip_address_split[1].split('.')[0])
    #
    #
    #
    #     if first_octet_ip > first_octet:
    #
    #         if first_octet_ip > second_octet:
    #             print(index, i)
    #             # get the next ip address_ index
    #



            # check next index in list







def add_white_list(ip_address):
    previous_scope = firewall_scopes_list()

    zero_IP = "0.0.0.0"
    last_IP = "255.255.255.255"

    if previous_scope != "Any":

        ip_address_scope_addition(previous_scope, ip_address)

        # print(previous_scope)

        # ip_address = ip_address.split('.')
        # last_octet = ip_address[-1]
        # other_remaining = ".".join(ip_address[0:3])
        #
        # first_range = f"{zero_IP}-{other_remaining}.{int(last_octet) - 1}"
        # second_range = f"{other_remaining}.{int(last_octet) + 1}-{last_IP}"
        #
        # new_scope = f'{previous_scope},{first_range},{second_range}'

        # netsh_allow_remote_address = f'''netsh advfirewall firewall set rule name="{firewall_rule_name}"  new remoteip={new_scope} '''
        # Popen(netsh_allow_remote_address)
        #

    else:
        netsh_allow_remote_address = f'''netsh advfirewall firewall set rule name="{firewall_rule_name}" new remoteip={ip_address} '''
        Popen(netsh_allow_remote_address)


def ip_address_exist_in_scope(ip_address):
    current_ip_scope = firewall_scopes_list()
    return ip_address in current_ip_scope


def remove_white_list(ip_address):
    previous_scope = firewall_scopes_list()

    if previous_scope != "Any":
        new_ip_address_scope = ','.join([ip for ip in previous_scope.split(",") if ip_address not in ip])

        netsh_allow_remote_address = f'''netsh advfirewall firewall set rule name="{firewall_rule_name}" dir=in new remoteip={new_ip_address_scope} '''
        Popen(netsh_allow_remote_address)


def enable_firewall_rule():
    netsh_add_firewall_command = f'''netsh advfirewall firewall set rule name="{firewall_rule_name}" new enable=yes '''
    call(netsh_add_firewall_command)


def disable_firewall_rule():
    netsh_add_firewall_command = f'''netsh advfirewall firewall set rule name="{firewall_rule_name}" new enable=no '''
    call(netsh_add_firewall_command)


def delete_firewall_rule():
    netsh_add_firewall_command = f'''netsh advfirewall firewall delete rule name="{firewall_rule_name}" '''
    in_command = Popen(netsh_add_firewall_command, stdout=PIPE, stderr=PIPE)
    output_message, _ = in_command.communicate()
    return "Ok." in output_message.decode().strip()
