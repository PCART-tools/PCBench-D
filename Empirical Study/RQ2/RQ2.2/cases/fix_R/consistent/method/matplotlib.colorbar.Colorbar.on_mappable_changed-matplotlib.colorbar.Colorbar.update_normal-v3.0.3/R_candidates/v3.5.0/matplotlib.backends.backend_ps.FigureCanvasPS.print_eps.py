    @_api.delete_parameter("3.5", "args")
    def print_eps(self, outfile, *args, **kwargs):
        return self._print_ps(outfile, 'eps', **kwargs)
