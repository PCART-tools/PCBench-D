    @deprecate_kwarg(old_arg_name='n', new_arg_name='repeats')
    def repeat(self, repeats, *args, **kwargs):
        nv.validate_repeat(args, kwargs)
        return MultiIndex(levels=self.levels,
                          labels=[label.view(np.ndarray).repeat(repeats)
                                  for label in self.labels], names=self.names,
                          sortorder=self.sortorder, verify_integrity=False)
