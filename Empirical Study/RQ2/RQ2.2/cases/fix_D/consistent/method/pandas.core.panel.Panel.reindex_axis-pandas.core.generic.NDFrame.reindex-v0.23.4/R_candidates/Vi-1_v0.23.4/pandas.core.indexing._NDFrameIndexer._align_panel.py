    def _align_panel(self, indexer, df):
        # TODO: is_frame, is_panel are unused
        is_frame = self.obj.ndim == 2  # noqa
        is_panel = self.obj.ndim >= 3  # noqa
        raise NotImplementedError("cannot set using an indexer with a Panel "
                                  "yet!")
