import scapy
from scapy.all import IP, TCP, UDP, rdpcap
from collections import defaultdict

TCP_EXPIRATION = 240  # 2x typical MSL (Maximum Segment Lifetime) for TCP
UDP_EXPIRATION = 600 # Sufficiently long for UDP

def assign_flow_ids_to_packets(truncated_packets):
    packets_by_hash = defaultdict(list)
    for packet in truncated_packets:
        #packet.pseudo_hash = generate_pseudo_hash(packet)  # Ensure each packet has a pseudo_hash
        if packet.pseudo_hash is not None:
            packets_by_hash[packet.pseudo_hash].append(packet)

    print(f"hash groups: {len(packets_by_hash)}")
    global_flow_id = 1
    flow_start_timestamp = {}  # Dictionary to store the initial timestamp for each flow
    first_packet_src_ip = None  # Reset at the beginning of processing

    fin_count = defaultdict(int)  # Tracks the number of FIN flags seen in each flow

    for hash_group in packets_by_hash.values():
        hash_group.sort(key=lambda pkt: pkt.timestamp)
        #print(f"Hash group: {hash_group}")

        last_timestamp = None
        new_flow_needed = False  # Flag to indicate if a new flow is needed

        for packet in hash_group:
            if global_flow_id not in flow_start_timestamp:
                flow_start_timestamp[global_flow_id] = packet.timestamp
                first_packet_src_ip = packet.src_ip

            if last_timestamp is not None:
                time_since_last_packet = packet.timestamp - last_timestamp
            else:
                time_since_last_packet = 0

            # Determine the expiration time based on the type of packet
            expiration_time = TCP_EXPIRATION if packet.tcp else UDP_EXPIRATION

            if time_since_last_packet >= expiration_time or new_flow_needed:
                # Handle expiration or post-second FIN new flow
                global_flow_id += 1
                flow_start_timestamp[global_flow_id] = packet.timestamp
                first_packet_src_ip = packet.src_ip  # Start new flow with the current packet IP
                new_flow_needed = False
                fin_count[global_flow_id] = 0  # Reset FIN counter for the new flow

            if packet.fin: # it has to be on the end of the function, because we want next packet for this hash (after double FIN) to be assigned to new flow
                fin_count[global_flow_id] += 1
                # Only end the flow after the second FIN flag in the same flow
                if fin_count[global_flow_id] >= 2:
                    new_flow_needed = True # TODO: False only for testing, must be True !


            packet.flow_id = global_flow_id
            packet.direction = 1 if packet.src_ip == first_packet_src_ip else 2
            last_timestamp = packet.timestamp

    return truncated_packets
