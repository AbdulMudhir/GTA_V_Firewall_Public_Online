from scapy.all import get_if_addr, get_if_list, conf, AsyncSniffer

network_interface = get_if_list()

host_ip_address = get_if_addr(conf.iface)

ip_addresses = []


def ip_address_scanned(packet):
    ip_address = packet.sprintf("{IP:%IP.src%}")

    if ip_address not in ip_addresses and ip_address != host_ip_address:
        ip_addresses.append(ip_address)


scan_ip_address = AsyncSniffer(iface=conf.iface, prn=ip_address_scanned,
                 filter="udp and port 6672 or port 61455 or port 61457 or port 61456 or port 61458", count=30)
