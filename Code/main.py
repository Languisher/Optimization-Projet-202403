from CyclistState import CyclistState


if __name__ == "__main__":
    cyclist = CyclistState(position=0, velocity=5, awc=20000)  # Initial state
    dt = 1  # Time step in seconds
    slope = 0.05  # Slope of the course (5% uphill)
    power_output = 350  # Power output in Watts

    # Simulate changes for a single timestep
    cyclist.change_position(dt)
    cyclist.change_velocity(power_output, slope, dt)
    cyclist.change_awc(power_output, dt)

    print(cyclist)