    @property
    def output_args(self):
        extra_args = (self.extra_args if self.extra_args is not None
                      else mpl.rcParams[self._args_key])
        return [*extra_args, self.outfile]
