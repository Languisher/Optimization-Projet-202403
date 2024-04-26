class Route:
    def __init__(self, segments, delta_s=10):
        """
        Initializes a new Route instance.

        Parameters:
            segments (list of tuples): Each tuple contains information about a segment
                                       in the form (segment_distance, segment_inclination_angle, mu).
            delta_s (float): Distance interval to store information, default is 10 meters.
        """
        self.segments = segments
        self.inclination_angle_list = []
        self.distance_list = []
        self.mu_list = []
        self.road_info_list = []  # List to store road information for each 10m segment
        self.delta_s = delta_s
        
        cumulative_distance = 0
        for segment in segments:
            segment_distance, segment_inclination_angle, mu = segment
            self.inclination_angle_list.append(segment_inclination_angle)
            self.mu_list.append(mu)
            
            num_subsegments = int(segment_distance / delta_s)
            remaining_distance = segment_distance
            for _ in range(num_subsegments):
                current_segment_distance = min(remaining_distance, delta_s)
                self.road_info_list.append((cumulative_distance + current_segment_distance, segment_inclination_angle, mu))
                remaining_distance -= current_segment_distance
                cumulative_distance += current_segment_distance

        self.distance_list = [segment[0] for segment in segments]

    def total_distance(self):
        """Returns the total distance of the route."""
        return sum(self.distance_list)

    def max_inclination(self):
        """Returns the maximum inclination angle in the route."""
        return max(self.inclination_angle_list)

    def __str__(self):
        route_info = "------------------ Input Route Info ------------------\n"
        for i, (distance, inclination, mu) in enumerate(self.road_info_list):
            route_info += f"Segment {i+1}: Distance = {distance} km, Inclination = {inclination} degrees, Friction_coef = {mu}\n"
        return route_info


if __name__ == "__main__":
    rout = Route(((50, 0, 0.015),  # Each tuple represents a segment: (distance in meters, incline angle in degrees, friction coefficient)
                (20, 30, 0.015),
                (50, -10, 0.015)))
    
    print(rout)
