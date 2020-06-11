from scapy.all import get_if_addr, conf, AsyncSniffer, get_windows_if_list


def network_interfaces():
    network_interface_name = []
    network_interface_description = []

    for network_interface in get_windows_if_list():
        network_interface_name.append(network_interface['name'])
        network_interface_description.append(network_interface['description'])

    return network_interface_name, network_interface_description


host_ip_address = get_if_addr(conf.iface)
ip_addresses = []


def ip_address_scanned(packet):

    ip_address = packet.sprintf("{IP:%IP.src%}")


    if ip_address not in ip_addresses and ip_address != host_ip_address:
        ip_addresses.append(ip_address)




def scan_ip_address(interface=conf.iface):

    ip_addresses =  []


    sniffer = AsyncSniffer(iface=interface, prn=lambda packet: ip_addresses.append(
        packet.sprintf("{IP:%IP.src%}")) if packet.sprintf("{IP:%IP.src%}") not in ip_addresses and
                                            packet.sprintf("{IP:%IP.src%}") != host_ip_address else None
                                                                                   ,
                           filter="udp and port 6672 or port 61455 or port 61457 or port 61456 or port 61458",
                           count=200)

    sniffer.start()
    sniffer.join(timeout=1)

    return ip_addresses
