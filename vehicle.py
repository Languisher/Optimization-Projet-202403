class Vehicle:
    def __init__(self, mass, frontal_area, velocity_init, energy_left, velocity_max, energy_max, output_power=0, covered_distance=0):
        """
        Initializes a new Vehicle instance.

        Parameters:
            mass (float): Mass of the vehicle in kilograms.
            frontal_area (float): Frontal area of the vehicle in square meters.
            velocity_init (float): Initial velocity of the vehicle in meters per second.
            energy_left (float): Initial energy left in the vehicle in joules.
            velocity_max (float): Maximum velocity vehicle can reach in meters per second.
            energy_max (float): Maximum energy capacity of the vehicle in joules.
            output_power (float): Current output power of the vehicle in watts. Default is 0.
            covered_distance (float): Total distance covered by the vehicle in meters. Default is 0.
        """
        self.mass = mass
        self.frontal_area = frontal_area
        self.velocity = velocity_init
        self.energy_left = energy_left
        self.velocity_max = velocity_max
        self.energy_max = energy_max
        self.output_power = output_power
        self.covered_distance = covered_distance

    def update_velocity(self, new_velocity):
        """Updates the vehicle's velocity, ensuring it does not exceed the maximum allowed velocity."""
        if new_velocity < 0:
            self.velocity = 0
        elif new_velocity > self.velocity_max:
            self.velocity = self.velocity_max
        else:
            self.velocity = new_velocity

    def consume_energy(self, energy_to_consume):
        """Decreases the energy left in the vehicle by the specified amount, not allowing negative energy."""
        if energy_to_consume > self.energy_left:
            self.energy_left = 0
        else:
            self.energy_left -= energy_to_consume

    def __str__(self):
        return f"------------------ Input Vehicle Info ------------------\n" \
               f"Covered Distance: {self.covered_distance}\n" \
               f"Velocity: {self.velocity}\n" \
               f"Energy Left: {self.energy_left}\n" \
               f"Output Power: {self.output_power}"
