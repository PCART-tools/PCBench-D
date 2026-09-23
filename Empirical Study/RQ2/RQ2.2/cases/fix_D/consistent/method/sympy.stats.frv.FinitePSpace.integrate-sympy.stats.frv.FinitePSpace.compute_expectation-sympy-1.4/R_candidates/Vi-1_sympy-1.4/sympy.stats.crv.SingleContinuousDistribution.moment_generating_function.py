    def moment_generating_function(self, t, **kwargs):
        """ Moment generating function """
        if len(kwargs) == 0:

            try:
                mgf = self._moment_generating_function(t)
                if mgf is not None:
                    return mgf
            except NotImplementedError:
                return None
        return self.compute_moment_generating_function(**kwargs)(t)
