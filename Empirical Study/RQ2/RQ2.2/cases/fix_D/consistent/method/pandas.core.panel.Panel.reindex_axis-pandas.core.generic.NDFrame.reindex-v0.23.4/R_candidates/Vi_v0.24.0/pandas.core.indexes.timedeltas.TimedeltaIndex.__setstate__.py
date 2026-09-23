    def __setstate__(self, state):
        """Necessary for making this object picklable"""
        if isinstance(state, dict):
            super(TimedeltaIndex, self).__setstate__(state)
        else:
            raise Exception("invalid pickle state")
