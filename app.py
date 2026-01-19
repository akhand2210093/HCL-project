from services.traffic import simulate_traffic_controller

if __name__ == "__main__":
    # Example 1: Random simulation for 8 cycles
    print("Random simulation (8 cycles):")
    simulate_traffic_controller(iterations=8, enable_print=True)

    # Example 2: Deterministic simulation using provided sensor sequences
    print("\nDeterministic simulation (4 cycles):")
    sensors_seq = [
        {"North": 5, "East": 2, "South": 3, "West": 1},
        {"North": 2, "East": 9, "South": 4, "West": 1},
        {"North": 0, "East": 0, "South": 0, "West": 0},  # no traffic
        {"North": 3, "East": 3, "South": 3, "West": 3},  # tie -> North chosen by order
    ]
    simulate_traffic_controller(iterations=4, sensor_sequences=sensors_seq, enable_print=True)

    # Example 3: Emergency override example
    print("\nEmergency example (East has emergency on cycle 2):")
    sensors_seq = [
        {"North": 1, "East": 1, "South": 1, "West": 1},
        {"North": 2, "East": 2, "South": 2, "West": 2},
    ]
    emergency_seq = [None, "East"]
    simulate_traffic_controller(iterations=2, sensor_sequences=sensors_seq, emergency_sequence=emergency_seq, enable_print=True)