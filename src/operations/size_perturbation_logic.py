import numpy as np
from scipy.stats import norm

class TruncatedPacket:
    def __init__(self, packet_id, timestamp, size, pseudo_hash, flow_id, direction, fragmented=0):
        self.packet_id = packet_id
        self.timestamp = timestamp
        self.size = size
        self.pseudo_hash = pseudo_hash
        self.flow_id = flow_id
        self.direction = direction
        self.fragmented = fragmented

def generate_weights(length, focus_point='middle', scaling_factor=1.0):
    """
    Generates weights for adjusting sizes or timestamps based on a normal distribution,
    focused on a specific part of the sequence with a scaling factor.
    """
    if length == 0:
        return np.ones(1)
    x = np.linspace(0, length, num=length)
    if focus_point == 'start':
        mean = length * 0.25
    elif focus_point == 'end':
        mean = length * 0.75
    else:  # 'middle'
        mean = length / 2
    std_dev = length / 10  # Control the spread of the influence
    weights = norm.pdf(x, loc=mean, scale=std_dev)
    if np.max(weights) == 0:
        # If the maximum weight is 0, avoid division by zero.
        return np.full(length, scaling_factor)
    weights /= np.max(weights)  # Normalize
    weights = weights * (scaling_factor - 1) + 1  # Adjust scaling
    return weights

def adjust_packet_size(truncated_packets, flow_id, direction, method='uniform', scaling_factor=1.0, focus_point='middle'):
    """
    Adjusts the size of packets within a specified flow_id and direction. If the target size is smaller than the
    original size, considers fragmentation based on thresholds and physical limitations. If the target size is larger,
    increases the size up to a maximum limit without exceeding 1500 bytes.
    
    Parameters:
    - truncated_packets: A list of TruncatedPacket objects to be adjusted.
    - flow_id: The specific flow_id for which the size adjustment is applied.
    - direction: The direction of packets to include ('0' - bidirect., '1' for src->dst, '2' for dst->src).
    - method: Type of adjustment method ('uniform', 'normal').
    - scaling_factor: Scaling factor for the size adjustment.
    - focus_point: Specifies the focus point for 'normal' distribution adjustment ('start', 'middle', 'end').
    """
    if direction == 0:
        filtered_packets = [p for p in truncated_packets if p.flow_id == flow_id]
    else:
        filtered_packets = [p for p in truncated_packets if p.flow_id == flow_id and p.direction == direction]
        
    num_packets = len(filtered_packets)

    if method == 'normal':
        weights = generate_weights(num_packets, focus_point=focus_point, scaling_factor=scaling_factor)
    else:
        weights = np.full(num_packets, scaling_factor)

    for i, packet in enumerate(filtered_packets):
        weight = weights[min(i, len(weights) - 1)]
        target_size = packet.size * weight

        # Handling size increase within limits
        if target_size > packet.size:
            packet.size = min(int(target_size), 1500)
        
        # Handling potential fragmentation when decreasing size
        elif target_size < packet.size:
            if packet.size >= 300 and target_size < packet.size * 1 / 4: # 300 = 4 * 75 (established min)
                packet.fragmented = 2 # Eligible for 4-way fragmentation
            elif packet.size >= 150 and target_size < packet.size * 3 / 4: # 150 = 2 * 75 (established min)
                packet.fragmented = 1  # Eligible for 2-way fragmentation
            
            else:
                packet.fragmented = 0
    
    return truncated_packets
