import nfstream
import scapy
from scapy.all import IP, TCP, UDP, rdpcap

TCP_EXPIRATION = 240.0
UDP_EXPIRATION = 240.0


def generate_pseudo_hash(entity):
    if isinstance(entity, nfstream.flow.NFlow):
        elements = [
            hash(entity.src_ip),
            hash(entity.dst_ip),
            int(entity.src_port),
            int(entity.dst_port),
            int(entity.protocol),
        ]

    # elif isinstance(entity, pyshark.packet.packet.Packet):
    #    elements = [hash(entity.ip.src), hash(entity.ip.dst), int(entity[entity.transport_layer].srcport), int(entity[entity.transport_layer].dstport), int(entity.ip.proto)]

    elif isinstance(entity, scapy.layers.l2.Ether):
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
    from collections import defaultdict

    # Group packets by pseudo_hash
    packets_by_hash = defaultdict(list)
    for packet in truncated_packets:
        packets_by_hash[packet.pseudo_hash].append(packet)

    global_flow_id = 1  # Initialize global flow ID

    for hash_group in packets_by_hash.values():
        # Sort packets within each group by timestamp
        hash_group.sort(key=lambda pkt: pkt.timestamp)

        first_packet_src_ip = None  # Source IP of the first packet in a flow
        last_timestamp = None  # Timestamp of the last packet
        waiting_for_new_flow = False  # Indicates if we are waiting to start a new flow

        for i, packet in enumerate(hash_group):
            # Check conditions for ending the current flow
            timeout_condition = (
                packet.tcp
                and last_timestamp is not None
                and (packet.timestamp - last_timestamp) > TCP_EXPIRATION
            ) or (
                packet.udp
                and last_timestamp is not None
                and (packet.timestamp - last_timestamp) > UDP_EXPIRATION
            )
            fin_condition = packet.tcp and packet.fin and not waiting_for_new_flow

            if timeout_condition or fin_condition:
                if timeout_condition:  # New flow starts after a timeout, not after FIN
                    waiting_for_new_flow = True
                if fin_condition:  # After FIN, we're still in the same flow
                    waiting_for_new_flow = False

            if (
                waiting_for_new_flow and not packet.fin
            ):  # New flow starts after FIN or timeout
                global_flow_id += 1
                waiting_for_new_flow = False  # Reset waiting for new flow

            if (
                not first_packet_src_ip or waiting_for_new_flow
            ):  # Setting for a new flow
                first_packet_src_ip = packet.src_ip

            packet.flow_id = global_flow_id
            packet.direction = 1 if packet.src_ip == first_packet_src_ip else 2

            last_timestamp = packet.timestamp  # Update the timestamp of the last packet

            # If it's the last packet in the hash group, ensure we end the current flow
            if i == len(hash_group) - 1:
                global_flow_id += 1
                waiting_for_new_flow = False

    return truncated_packets
