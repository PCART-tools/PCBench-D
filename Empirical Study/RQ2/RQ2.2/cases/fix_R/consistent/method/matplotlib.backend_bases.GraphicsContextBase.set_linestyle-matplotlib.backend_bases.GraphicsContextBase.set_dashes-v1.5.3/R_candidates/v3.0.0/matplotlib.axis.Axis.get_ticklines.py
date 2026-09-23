    def get_ticklines(self, minor=False):
        'Return the tick lines as a list of Line2D instances'
        if minor:
            return self.get_minorticklines()
        return self.get_majorticklines()
