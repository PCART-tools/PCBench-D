    def get_ticklines(self, minor=False):
        r"""Return this Axis' tick lines as a list of `.Line2D`\s."""
        if minor:
            return self.get_minorticklines()
        return self.get_majorticklines()
