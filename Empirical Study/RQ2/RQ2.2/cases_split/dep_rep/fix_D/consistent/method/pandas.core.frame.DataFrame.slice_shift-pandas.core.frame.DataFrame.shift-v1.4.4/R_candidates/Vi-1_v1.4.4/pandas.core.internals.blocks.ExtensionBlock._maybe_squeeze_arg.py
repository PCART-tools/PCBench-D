    def _maybe_squeeze_arg(self, arg):
        """
        If necessary, squeeze a (N, 1) ndarray to (N,)
        """
        # e.g. if we are passed a 2D mask for putmask
        if isinstance(arg, np.ndarray) and arg.ndim == self.values.ndim + 1:
            # TODO(EA2D): unnecessary with 2D EAs
            assert arg.shape[1] == 1
            arg = arg[:, 0]
        return arg
