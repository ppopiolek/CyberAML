#import nfstream
import scapy
from scapy.all import IP, TCP, UDP, rdpcap
from collections import defaultdict

TCP_EXPIRATION = 240000000
UDP_EXPIRATION = 240000000


def generate_pseudo_hash(entity):
    '''
    if isinstance(entity, nfstream.flow.NFlow):
        elements = [
            hash(entity.src_ip),
            hash(entity.dst_ip),
            int(entity.src_port),
            int(entity.dst_port),
            int(entity.protocol),
        ]
        '''

    # elif isinstance(entity, pyshark.packet.packet.Packet):
    #    elements = [hash(entity.ip.src), hash(entity.ip.dst), int(entity[entity.transport_layer].srcport), int(entity[entity.transport_layer].dstport), int(entity.ip.proto)]

    if isinstance(entity, scapy.layers.l2.Ether):
        if entity.haslayer(TCP):
            elements = [
                hash(entity[IP].src),
                hash(entity[IP].dst),
                int(entity[TCP].sport),
                int(entity[TCP].dport),
                int(entity[IP].proto),
            ]
        elif entity.haslayer(UDP):
            elements = [
                hash(entity[IP].src),
                hash(entity[IP].dst),
                int(entity[UDP].sport),
                int(entity[UDP].dport),
                int(entity[IP].proto),
            ]
    else:
        print("ERROR: not a flow nor packet")

    return sum(elements)

def assign_flow_ids_to_packets(truncated_packets):
    packets_by_hash = defaultdict(list)
    for packet in truncated_packets:
        #packet.pseudo_hash = generate_pseudo_hash(packet)  # Upewnij się, że każdy pakiet ma pseudo_hash
        packets_by_hash[packet.pseudo_hash].append(packet)

    global_flow_id = 1
    flow_start_timestamp = {}  # Słownik do przechowywania początkowego znacznika czasu dla każdego przepływu

    for hash_group in packets_by_hash.values():
        hash_group.sort(key=lambda pkt: pkt.timestamp)

        first_packet_src_ip = None
        last_timestamp = None
        waiting_for_new_flow = False

        for i, packet in enumerate(hash_group):
            # Dodajemy początkowy znacznik czasu dla przepływu, jeśli jeszcze go nie ma
            if global_flow_id not in flow_start_timestamp:
                flow_start_timestamp[global_flow_id] = packet.timestamp

            # Oblicz czas trwania przepływu
            flow_duration = packet.timestamp - flow_start_timestamp[global_flow_id]

            # Zaktualizowane warunki uwzględniające czas trwania przepływu
            timeout_condition = (
                (packet.tcp or packet.udp) and
                last_timestamp is not None and
                (packet.timestamp - last_timestamp > TCP_EXPIRATION or packet.timestamp - last_timestamp > UDP_EXPIRATION)
            )
            fin_condition = packet.tcp and packet.fin and not waiting_for_new_flow
            #fin_condition = 0

            if timeout_condition or fin_condition:
                waiting_for_new_flow = True if timeout_condition else False

            if waiting_for_new_flow and not packet.fin:
                global_flow_id += 1
                waiting_for_new_flow = False
                flow_start_timestamp[global_flow_id] = packet.timestamp  # Rozpoczęcie nowego przepływu

            if not first_packet_src_ip or waiting_for_new_flow:
                first_packet_src_ip = packet.src_ip

            packet.flow_id = global_flow_id
            packet.direction = 1 if packet.src_ip == first_packet_src_ip else 2

            last_timestamp = packet.timestamp

            if i == len(hash_group) - 1:
                global_flow_id += 1
                waiting_for_new_flow = False

    return truncated_packets

