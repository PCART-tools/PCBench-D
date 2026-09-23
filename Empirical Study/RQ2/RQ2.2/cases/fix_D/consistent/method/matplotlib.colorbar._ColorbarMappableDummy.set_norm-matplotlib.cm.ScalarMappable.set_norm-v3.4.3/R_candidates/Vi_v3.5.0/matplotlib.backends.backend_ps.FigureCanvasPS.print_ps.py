    @_api.delete_parameter("3.5", "args")
    def print_ps(self, outfile, *args, **kwargs):
        return self._print_ps(outfile, 'ps', **kwargs)
