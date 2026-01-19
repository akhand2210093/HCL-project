from services.traffic import simulate_traffic_controller

def prompt_user_for_counts() -> dict:
    """Ask the user for counts for each direction (press Enter to use 0)."""
    directions = ["North", "East", "South", "West"]
    result = {}
    for d in directions:
        while True:
            raw = input(f"Enter vehicle count for {d} (or Enter for 0): ").strip()
            if raw == "":
                result[d] = 0
                break
            try:
                result[d] = int(raw)
                if result[d] < 0:
                    print("Please enter a non-negative integer.")
                    continue
                break
            except ValueError:
                print("Please enter a valid integer or press Enter for 0.")
    return result

def run_interactive_cycles(cycles: int = 3):
    sensor_seq = []
    for i in range(cycles):
        print(f"\n--- Cycle {i+1} input ---")
        counts = prompt_user_for_counts()
        sensor_seq.append(counts)
    simulate_traffic_controller(iterations=cycles, sensor_sequences=sensor_seq, enable_print=True)

if __name__ == "__main__":
    print("Interactive traffic controller input. You will be prompted for counts.")
    # Change cycles to however many cycles you want to input
    run_interactive_cycles(cycles=3)