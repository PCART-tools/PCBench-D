    def get_majorticklocs(self):
        "Get the major tick locations in data coordinates as a numpy array"
        return self.major.locator()
