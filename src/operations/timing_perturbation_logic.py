import numpy as np
from scipy.stats import norm
import copy


def generate_weights(length, mean, stddev):
    """
    Generates weights for adjusting deltas based on a normal distribution with specified mean and stddev.
    """
    x = np.linspace(0, length, num=length)
    weights = norm.pdf(x, loc=mean, scale=stddev)
    weights /= np.max(weights)  # Normalize
    return weights

def rebuild_timestamps(flow_packets, adjusted_deltas):
    """
    Rebuilds timestamps from adjusted deltas for a sequence of packets.
    """
    timestamp = flow_packets[0].timestamp
    for i, delta in enumerate(adjusted_deltas):
        timestamp += delta
        if i + 1 < len(flow_packets):
            flow_packets[i + 1].timestamp = timestamp

def apply_uniform_perturbation_deepcopy(truncated_packets, flow_id, scaling_factor=1.0):
    """
    Uniformly adjusts timestamps within a specified flow_id, ensuring no adjusted delta exceeds 239.
    """
    flow_packets = sorted([p for p in truncated_packets if p.flow_id == flow_id], key=lambda p: p.timestamp)
    if not flow_packets:
        return truncated_packets

    flow_packets_copy = copy.deepcopy(flow_packets)
    
    # Calculate and adjust deltas
    deltas = np.diff([p.timestamp for p in flow_packets_copy])
    adjusted_deltas = np.minimum(deltas * scaling_factor, 239)

    # Rebuild timestamps from adjusted deltas
    rebuild_timestamps(flow_packets_copy, adjusted_deltas)
    return flow_packets_copy

def apply_normal_perturbation_deepcopy(truncated_packets, flow_id, mean, stddev):
    """
    Adjusts timestamps within a specified flow_id based on a normal distribution with specified mean and stddev,
    ensuring no adjusted delta exceeds 239.
    """
    flow_packets = sorted([p for p in truncated_packets if p.flow_id == flow_id], key=lambda p: p.timestamp)
    if not flow_packets:
        return truncated_packets
    
    flow_packets_copy = copy.deepcopy(flow_packets)

    deltas = np.diff([p.timestamp for p in flow_packets_copy])
    weights = generate_weights(len(deltas), mean, stddev)
    adjusted_deltas = np.minimum(deltas * weights, 239)

    # Rebuild timestamps from adjusted deltas
    rebuild_timestamps(flow_packets_copy, adjusted_deltas)
    return flow_packets_copy


def apply_time_perturbation_with_focus_deepcopy(truncated_packets, flow_id, method, focus_point='middle', scaling_factor=1.0):
    """
    Applies perturbation with a focus point and scaling factor for the 'normal' method, automatically calculating
    mean and stddev based on the focus point.
    """
    num_packets = sum(1 for p in truncated_packets if p.flow_id == flow_id)
    if num_packets < 2:
        print("Not enough packets to apply perturbation.")
        return truncated_packets

    # Determine mean and stddev based on focus_point for the normal distribution
    if focus_point == 'start':
        mean = num_packets * 0.25
    elif focus_point == 'end':
        mean = num_packets * 0.75
    else:  # Default to 'middle'
        mean = num_packets / 2
    if isinstance(scaling_factor, str):
        raise ValueError(f"scaling_factor can't be string: {scaling_factor}")
    # Use a scaling factor to adjust the spread of the distribution
    stddev = max(num_packets / (10 * scaling_factor), 1)  # Ensure stddev is at least 1 to avoid division by zero

    if method == 'normal':
        return apply_normal_perturbation_deepcopy(truncated_packets, flow_id, mean, stddev)
    elif method == 'uniform':
        return apply_uniform_perturbation_deepcopy(truncated_packets, flow_id, scaling_factor)
    else:
        raise ValueError(f"Unsupported perturbation method: {method}")
    
    
def apply_time_perturbation_with_focus(truncated_packets, flow_id, method, focus_point='middle', scaling_factor=1.0):
    """
    Applies perturbation with a focus point and scaling factor for the 'normal' method, automatically calculating
    mean and stddev based on the focus point.
    """
    num_packets = sum(1 for p in truncated_packets if p.flow_id == flow_id)
    if num_packets < 2:
        print("Not enough packets to apply perturbation.")
        return truncated_packets

    # Determine mean and stddev based on focus_point for the normal distribution
    if focus_point == 'start':
        mean = num_packets * 0.25
    elif focus_point == 'end':
        mean = num_packets * 0.75
    else:  # Default to 'middle'
        mean = num_packets / 2
    if isinstance(scaling_factor, str):
        raise ValueError(f"scaling_factor can't be string: {scaling_factor}")
    # Use a scaling factor to adjust the spread of the distribution
    stddev = max(num_packets / (10 * scaling_factor), 1)  # Ensure stddev is at least 1 to avoid division by zero

    if method == 'normal':
        return apply_normal_perturbation(truncated_packets, flow_id, mean, stddev)
    elif method == 'uniform':
        return apply_uniform_perturbation(truncated_packets, flow_id, scaling_factor)
    else:
        raise ValueError(f"Unsupported perturbation method: {method}")
    
    
def apply_uniform_perturbation(truncated_packets, flow_id, scaling_factor=1.0):
    """
    Uniformly adjusts timestamps within a specified flow_id, ensuring no adjusted delta exceeds 239.
    """
    flow_packets = sorted([p for p in truncated_packets if p.flow_id == flow_id], key=lambda p: p.timestamp)
    if not flow_packets:
        return truncated_packets

    
    # Calculate and adjust deltas
    deltas = np.diff([p.timestamp for p in flow_packets])
    adjusted_deltas = np.minimum(deltas * scaling_factor, 239)

    # Rebuild timestamps from adjusted deltas
    rebuild_timestamps(flow_packets, adjusted_deltas)
    return truncated_packets

def apply_normal_perturbation(truncated_packets, flow_id, mean, stddev):
    """
    Adjusts timestamps within a specified flow_id based on a normal distribution with specified mean and stddev,
    ensuring no adjusted delta exceeds 239.
    """
    flow_packets = sorted([p for p in truncated_packets if p.flow_id == flow_id], key=lambda p: p.timestamp)
    if not flow_packets:
        return truncated_packets
    

    deltas = np.diff([p.timestamp for p in flow_packets])
    weights = generate_weights(len(deltas), mean, stddev)
    adjusted_deltas = np.minimum(deltas * weights, 239)

    # Rebuild timestamps from adjusted deltas
    rebuild_timestamps(flow_packets, adjusted_deltas)
    return truncated_packets