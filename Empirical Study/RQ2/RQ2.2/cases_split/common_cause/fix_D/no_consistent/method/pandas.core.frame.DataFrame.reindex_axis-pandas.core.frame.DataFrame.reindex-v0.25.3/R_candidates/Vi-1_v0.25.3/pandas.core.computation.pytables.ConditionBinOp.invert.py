    def invert(self):
        """ invert the condition """
        # if self.condition is not None:
        #    self.condition = "~(%s)" % self.condition
        # return self
        raise NotImplementedError(
            "cannot use an invert condition when " "passing to numexpr"
        )
