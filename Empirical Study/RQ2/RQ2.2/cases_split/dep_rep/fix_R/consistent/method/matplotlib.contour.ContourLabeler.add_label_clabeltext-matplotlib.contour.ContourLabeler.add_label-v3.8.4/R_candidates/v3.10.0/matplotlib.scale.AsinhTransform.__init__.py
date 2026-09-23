    def __init__(self, linear_width):
        super().__init__()
        if linear_width <= 0.0:
            raise ValueError("Scale parameter 'linear_width' " +
                             "must be strictly positive")
        self.linear_width = linear_width
