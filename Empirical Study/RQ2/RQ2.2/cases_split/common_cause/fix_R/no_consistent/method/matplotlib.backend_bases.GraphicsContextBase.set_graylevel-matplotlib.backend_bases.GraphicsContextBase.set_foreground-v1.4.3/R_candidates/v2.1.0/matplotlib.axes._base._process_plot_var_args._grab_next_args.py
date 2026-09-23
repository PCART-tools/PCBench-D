    def _grab_next_args(self, *args, **kwargs):
        while args:
            this, args = args[:2], args[2:]
            if args and isinstance(args[0], six.string_types):
                this += args[0],
                args = args[1:]
            for seg in self._plot_args(this, kwargs):
                yield seg
