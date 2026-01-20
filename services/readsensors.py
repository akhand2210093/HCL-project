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