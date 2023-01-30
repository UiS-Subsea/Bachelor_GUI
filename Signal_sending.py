# Importe socket først
import socket
from struct import *
import struct
import sys
# Bruke socket til å lage en "fresh"/tom socket som vi kan bygge på
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
# Bruker AF_INET for IPv4 versjon, kan potensielt bruke AP_INET6 for IPv6
# men spørs hvor relevant det er. Lage TCP socket for nå.

# Lager while loop som lar oss receive data
# hile True:
#    print(s.recvfrom(65))
# 65565 er bare en buffer size, der 655565 er max buffer size....


def ethernet_head(raw_data):
    dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
    dest_mac = get_mac_addr(dest)
    src_mac = get_mac_addr(src)
    proto = socket.htons(prototype)
    data = raw_data[14:]
    return dest_mac, src_mac, proto, data


def main():
    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    while True:
        raw_data, addr = s.recvfrom(65535)
        eth = ethernet(raw_data)
        print('\nEthernet Frame:')
        print('Destination: {}, Source: {}, Protocol: {}'.format(eth[0], eth[1],
                                                                 eth[2]))
        if eth[2] == 8:
            ipv4 = ipv4(ethp[4])
            print('\t - ' + 'IPv4 Packet:')
            print('\t\t - ' + 'Version: {}, Header Length: {}, TTL:
                  {}, '.format(ipv4[1], ipv4[2], ipv4[3]))
            print('\t\t - ' + 'Protocol: {}, Source: {}, Target:
                  {}'.format(ipv4[4], ipv4[5], ipv4[6]))


def ipv4_head(raw_data):
    version_header_length = raw_data[0]
    version = version_header_length >> 4
    header_length = (version_header_length & 15) * 4
    ttl, proto, src, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
    data = raw_data[header_length:]
    return version, header_length, ttl, proto, src, target, data


main()
