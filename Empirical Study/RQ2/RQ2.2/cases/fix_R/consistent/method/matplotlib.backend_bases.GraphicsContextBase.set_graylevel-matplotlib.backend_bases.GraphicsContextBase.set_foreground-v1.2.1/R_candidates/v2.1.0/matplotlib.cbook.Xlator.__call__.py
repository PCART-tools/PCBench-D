    def __call__(self, match):
        """ Handler invoked for each regex *match* """
        return self[match.group(0)]
