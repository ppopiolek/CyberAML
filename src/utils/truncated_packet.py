from .flow import generate_pseudo_hash
from scapy.all import IP, TCP, UDP, rdpcap


class TruncatedPacket:
    def __init__(
        self,
        packet_id,
        timestamp,
        size,
        pseudo_hash,
        flow_id,
        direction,
        src_ip,
        tcp,
        udp,
        fin,
        syn,
        rst,
        ack,
        psh,
        urg,
    ):
        self.packet_id = packet_id
        self.timestamp = timestamp
        self.size = size
        self.pseudo_hash = pseudo_hash
        self.flow_id = flow_id
        self.direction = direction
        self.src_ip = src_ip
        self.tcp = tcp
        self.udp = udp
        self.fin = fin
        self.syn = syn
        self.rst = rst
        self.ack = ack
        self.psh = psh
        self.urg = urg

    def __repr__(self):
        return (
            f"TruncatedPacket(packet_id={self.packet_id}, timestamp={self.timestamp}, size={self.size}, "
            f"pseudo_hash='{self.pseudo_hash}', flow_id={self.flow_id}, direction='{self.direction}', src_ip={self.src_ip}, "
            f"tcp={self.tcp}, udp={self.udp}, fin={self.fin}, syn={self.syn}, rst={self.rst}, ack={self.ack}, psh={self.psh}, urg={self.urg})"
        )


def create_truncated_packets_from_pcap(file_path):
    truncated_packets = []
    cap = rdpcap(file_path)

    for packet_number, scapy_packet in enumerate(cap, start=1):
        if IP in scapy_packet and (
            scapy_packet.haslayer(TCP) or scapy_packet.haslayer(UDP)
        ):
            pseudo_hash = generate_pseudo_hash(scapy_packet)

            tcp, udp, fin, syn, rst, ack, psh, urg = (
                0,
            ) * 8  # Initialize all flags to 0

            if scapy_packet.haslayer(TCP):
                tcp = 1
                flags = scapy_packet[TCP].flags
                fin = int(bool(flags & 0x01))
                syn = int(bool(flags & 0x02))
                rst = int(bool(flags & 0x04))
                ack = int(bool(flags & 0x10))
                psh = int(bool(flags & 0x08))
                urg = int(bool(flags & 0x20))

            udp = int(scapy_packet.haslayer(UDP))

            truncated_packet = TruncatedPacket(
                packet_id=packet_number * 10,  # According to schema
                timestamp=scapy_packet.time,  # Timestamp will need to have margin of error
                size=len(scapy_packet),
                pseudo_hash=pseudo_hash,
                flow_id=None,  # Later assignment
                direction=0,  # 0 - not yet analyzed, 1 - fwd, 2 - bwd
                src_ip=scapy_packet[IP].src,
                tcp=tcp,
                udp=udp,
                fin=fin,
                syn=syn,
                rst=rst,
                ack=ack,
                psh=psh,
                urg=urg,
            )
            truncated_packets.append(truncated_packet)

    return truncated_packets
