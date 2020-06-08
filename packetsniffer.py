from scapy.all import get_if_addr, get_if_list, conf, AsyncSniffer

network_interface = get_if_list()

host_ip_address = get_if_addr(conf.iface)

ip_addresses = []


def ip_address_scanned(packet):
    ip_address = packet.sprintf("{IP:%IP.src%}")

    if ip_address not in ip_addresses and ip_address != host_ip_address:
        ip_addresses.append(ip_address)


def scan_ip_address(interface = conf.iface):
    sniffer = AsyncSniffer(iface=interface, prn=ip_address_scanned,
                 filter="udp and port 6672 or port 61455 or port 61457 or port 61456 or port 61458", count=200)

    sniffer.start()
    sniffer.join()

    return ip_addresses
