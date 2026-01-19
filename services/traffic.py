import random
from typing import Dict, List, Optional, Tuple

DIRECTIONS = ["North", "East", "South", "West"]


def read_sensors(simulated: Optional[Dict[str, int]] = None) -> Dict[str, int]:
    """
    Read traffic sensor counts for each direction.
    If `simulated` dict is provided, use it. Otherwise, generate random counts (0-20).
    Returns a dict like {"North": 5, "East": 12, ...}
    """
    if simulated:
        # Ensure all directions are present
        return {d: int(simulated.get(d, 0)) for d in DIRECTIONS}
    # Simple random simulation
    return {d: random.randint(0, 20) for d in DIRECTIONS}


def detect_traffic(sensor_data: Optional[Dict[str, int]] = None) -> Dict[str, int]:
    """
    Wrapper that returns counts from sensors.
    Kept as a separate function for clarity and potential preprocessing.
    """
    return read_sensors(sensor_data)


def prioritize_direction(counts: Dict[str, int]) -> Tuple[str, int]:
    """
    Choose the direction with the maximum vehicles.
    Tie-breaking: choose the first direction with the max count in DIRECTIONS order.
    Returns (direction_name, count)
    """
    max_count = -1
    chosen = DIRECTIONS[0]
    for d in DIRECTIONS:
        c = counts.get(d, 0)
        if c > max_count:
            max_count = c
            chosen = d
    return chosen, max_count


def calculate_durations(max_count: int, total_count: int, min_green: int = 10, max_green: int = 60) -> int:
    """
    Calculate green duration (seconds) for chosen direction based on traffic proportion.
    - If no traffic, return min_green.
    - Otherwise scale between min_green and max_green by the proportion of the max_count to total_count.
    """
    if total_count <= 0:
        return min_green
    proportion = max_count / total_count
    duration = min_green + (max_green - min_green) * proportion
    return max(min_green, int(round(duration)))


def set_signal_state(green_direction: str, green_duration: int, yellow_duration: int = 3) -> Dict[str, Dict]:
    """
    Build a simple state representation for all signals.
    The chosen direction gets GREEN for green_duration then YELLOW for yellow_duration.
    Others are RED for the same cycle.
    """
    state = {}
    for d in DIRECTIONS:
        if d == green_direction:
            state[d] = {"color": "GREEN", "time": green_duration}
        else:
            state[d] = {"color": "RED", "time": green_duration + yellow_duration}
    # Add yellow step info (for completeness)
    state["_meta"] = {"yellow_duration": yellow_duration}
    return state


def update_timers(state: Dict[str, Dict], elapsed: int) -> Dict[str, Dict]:
    """
    Decrement timers by elapsed seconds. (Simple utility)
    Not heavily used in this simulation loop but provided for completeness.
    """
    for d in DIRECTIONS:
        t = state[d].get("time", 0)
        state[d]["time"] = max(0, t - elapsed)
        # If green time reaches 0, move to yellow or red in a real controller.
    return state


def emergency_override(counts: Dict[str, int], emergency_dir: Optional[str] = None) -> Optional[str]:
    """
    If an emergency direction is provided, immediately prioritize it.
    Return the emergency direction or None.
    """
    if emergency_dir and emergency_dir in DIRECTIONS:
        return emergency_dir
    return None


def log_state(logs: List[Dict], iteration: int, counts: Dict[str, int], chosen: str, durations: Dict[str, int]) -> List[Dict]:
    """
    Append a simple summary record to logs and return logs.
    """
    record = {
        "iteration": iteration,
        "counts": counts.copy(),
        "chosen": chosen,
        "durations": durations.copy()
    }
    logs.append(record)
    return logs


def visualize_state(state: Dict[str, Dict]) -> None:
    """
    Print a simple ASCII visualization of the signals.
    """
    lines = []
    for d in DIRECTIONS:
        color = state[d]["color"]
        t = state[d]["time"]
        lines.append(f"{d[:1]}:{color[:1]}({t}s)")
    # Example output: N:G(20) E:R(23) S:R(23) W:R(23)
    print(" | ".join(lines))


def simulate_traffic_controller(iterations: int = 10,
                                sensor_sequences: Optional[List[Dict[str, int]]] = None,
                                emergency_sequence: Optional[List[Optional[str]]] = None,
                                enable_print: bool = True) -> List[Dict]:
    """
    Run a simple simulation for `iterations` cycles.
    - sensor_sequences: optional list of dicts to use as sensors for each iteration.
    - emergency_sequence: optional list of emergency direction names (or None) for each iteration.
    Returns logs (list of records).
    """
    logs: List[Dict] = []
    for i in range(iterations):
        sensors = None
        if sensor_sequences and i < len(sensor_sequences):
            sensors = sensor_sequences[i]
        counts = detect_traffic(sensors)

        # Check emergency override
        emergency_dir = None
        if emergency_sequence and i < len(emergency_sequence):
            emergency_dir = emergency_sequence[i]
        override = emergency_override(counts, emergency_dir)

        if override:
            chosen = override
            chosen_count = counts.get(chosen, 0)
        else:
            chosen, chosen_count = prioritize_direction(counts)

        total = sum(counts.values())
        green_duration = calculate_durations(chosen_count, total)
        state = set_signal_state(chosen, green_duration)

        # Log and optionally print/visualize
        log_state(logs, i + 1, counts, chosen, {"green": green_duration, "yellow": state["_meta"]["yellow_duration"]})
        if enable_print:
            print(f"Cycle {i+1}: counts={counts}, chosen={chosen}, green={green_duration}s")
            visualize_state(state)
            print("-" * 60)

    return logs