    def get_minorticklocs(self):
        "Get the minor tick locations in data coordinates as a numpy array"
        return self.minor.locator()
