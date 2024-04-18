class Route:
    def __init__(self, segments):
        """
        Initializes a new Route instance.
        :param segments: A list of tuples, each representing a segment of the route.
                         Each tuple is (distance, incline), where 'distance' is the
                         length of the segment in meters, and 'incline' is the angle
                         of inclination in radians.
        """
        self.segments = segments
        self.total_distance = sum(segment[0] for segment in segments)
    
    def get_incline(self, distance):
        """
        Returns the incline (theta) at a given distance along the route.
        :param distance: The distance from the start of the route in meters.
        :return: The incline (theta) in radians at the given distance.
        """
        traveled = 0
        for segment_length, segment_incline in self.segments:
            if distance <= traveled + segment_length:
                return segment_incline
            traveled += segment_length
        return 0  # Return a default value if the distance exceeds the route length
