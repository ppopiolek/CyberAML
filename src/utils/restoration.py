import os

from scapy.all import (IP, TCP, Ether, Packet, Padding, PcapReader, PcapWriter,
                       Raw, fragment)
from scapy.fields import StrField


class StealthProtocol(Packet):
    name = "StealthProtocol"
    fields_desc = [StrField("padding", default="")]


def add_padding(packet, padding_size):
    padding = os.urandom(padding_size)

    stealth_protocol_instance = StealthProtocol(padding=padding)

    packet = packet / stealth_protocol_instance

    return packet


def change_packet_timestamp(packet, new_timestamp):
    packet.time = new_timestamp
    return packet


def fragment_packet(packet, fragment_size):
    return fragment(packet, fragsize=fragment_size)


def split_flow(packet):
    # Ensure the packet is an IP packet containing a TCP layer
    if IP in packet and TCP in packet:
        # Create a new packet with the FIN flag, copying IP addresses and ports from the original packet
        fin_packet = (
            Ether(src=packet[Ether].src, dst=packet[Ether].dst)
            / IP(src=packet[IP].src, dst=packet[IP].dst)
            / TCP(sport=packet[TCP].sport, dport=packet[TCP].dport, flags="F")
        )
        fin_packet.time = packet.time + 0.00001
        print(f"fin:{fin_packet.time}")
        return fin_packet
    # Else it has to be UDP:)
    else:
        fin_packet = (
            Ether(src=packet[Ether].src, dst=packet[Ether].dst)
            / IP(src=packet[IP].src, dst=packet[IP].dst)
            / TCP(sport=packet[UDP].sport, dport=packet[UDP].dport, flags="F")
        )
        return fin_packet


def dummy_packet(packet, size):
    if IP in packet:
        dummy = Ether(src=packet[Ether].src, dst=packet[Ether].dst) / IP(
            src=packet[IP].src, dst=packet[IP].dst
        )

        if TCP in packet:
            dummy /= TCP(sport=packet[TCP].sport, dport=packet[TCP].dport)
        elif UDP in packet:
            dummy /= UDP(sport=packet[UDP].sport, dport=packet[UDP].dport)
        else:
            return "The packet does not contain a TCP or UDP layer."

        # Add a payload to meet the desired size, considering the size of the headers
        payload_size = max(0, size - len(dummy))
        dummy /= "0" * payload_size
        dummy.time = packet.time + 0.000001

        return dummy
    else:
        return "The packet does not contain an IP layer."


# TODO: maybe block dummy_flags for UDP flows
def dummy_flag(packet, flags):
    if IP in packet:
        src_port, dst_port = 0, 0

        if TCP in packet:
            src_port, dst_port = packet[TCP].sport, packet[TCP].dport
        elif UDP in packet:
            src_port, dst_port = packet[UDP].sport, packet[UDP].dport
        else:
            return "The packet does not contain a TCP or UDP layer."

        # Generate a TCP packet with the specified flags, using ports from the original packet
        flagged_packet = (
            Ether(src=packet[Ether].src, dst=packet[Ether].dst)
            / IP(src=packet[IP].src, dst=packet[IP].dst)
            / TCP(sport=src_port, dport=dst_port, flags=flags)
        )
        flagged_packet.time = packet.time + 0.000001

        return flagged_packet
    else:
        return "The packet does not contain an IP layer."


def modify_and_write_packets_one_by_one(
    original_pcap, modified_pcap, truncated_packets=None
):

    if os.path.exists(modified_pcap):
        os.remove(modified_pcap)

    writer = PcapWriter(modified_pcap, append=True, sync=True)
    truncated_packets_dict = {tp.packet_id: tp for tp in truncated_packets}

    with PcapReader(original_pcap) as reader:
        for i, packet in enumerate(reader):
            if IP in packet:
                packet_id = i + 1
                if packet_id in truncated_packets_dict:
                    tp = truncated_packets_dict[packet_id]

                    # Change timestamp if necessary
                    packet.time = tp.timestamp

                    # Adjust packet size by adding padding or fragmenting
                    packet_length = len(packet)
                    if packet_length < tp.size:
                        packet = add_padding(packet, tp.size - packet_length)

                    # Fragmentation
                    if tp.fragmented == 1:
                        packet = fragment_packet(packet, int(tp.size/2))
                    elif tp.fragmented == 2:
                        packet = fragment_packet(packet, int(tp.size/4))

                    # TEST CASE SCENARIOS WHICH WORKED:

                    # CHANGE TIMESTAMP
                    # new_timestamp = packet.time + 100000000
                    # packet = change_packet_timestamp(packet, new_timestamp)

                    # PACKET FRAGMENTATION
                    # fragment_size = 500
                    # packet = fragment_packet(packet, fragment_size)

                    # PADDING
                    # padding_size = 200
                    # packet = add_padding(packet, padding_size)

                    # SPLIT FLOW
                    # writer.write(packet) - dont send afterwards
                    # splt = split_flow(packet)
                    # writer.write(splt)

                    # DUMMY PACKET
                    # writer.write(packet) - dont send afterwards
                    # writer.write(dummy_packet(packet, 1000))

                    # DUMMY FLAG
                    # writer.write(packet) - donr send afterwards
                    # writer.write(dummy_flag(packet, "SA"))

                    #TODO: test
                    #writer.write(packet) # <--- don't write packet if not in truncated_packets list
            writer.write(packet) # <--- always write packet - even if not in truncated_packets

    writer.close()
