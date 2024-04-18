class Route:
    def __init__(self, segments):
        """
        Initializes a new Route instance.

        Parameters:
            segments (list of tuples): Each tuple contains information about a segment
                                       in the form (segment_distance, segment_inclination_angle, mu).
        """
        self.segments = segments
        self.inclination_angle_list = []
        self.distance_list = []
        self.mu_list = []

        for segment in segments:
            segment_distance, segment_inclination_angle, mu = segment
            
            self.inclination_angle_list.append(segment_inclination_angle)
            self.distance_list.append(segment_distance)
            self.mu_list.append(mu)
    
    def total_distance(self):
        """Returns the total distance of the route."""
        return sum(self.distance_list)

    def max_inclination(self):
        """Returns the maximum inclination angle in the route."""
        return max(self.inclination_angle_list)

    def __str__(self):
        route_info = "------------------ Input Route Info ------------------\n"
        for i, (distance, inclination, mu) in enumerate(zip(self.distance_list, self.inclination_angle_list, self.mu_list)):
            route_info += f"Segment {i+1}: Distance = {distance} m, Inclination = {inclination} degrees, Friction_coef = {mu}\n"
        return route_info
