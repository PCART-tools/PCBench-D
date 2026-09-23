    def _align_panel(self, indexer, df):
        is_frame = self.obj.ndim == 2
        is_panel = self.obj.ndim >= 3
        raise NotImplementedError("cannot set using an indexer with a Panel "
                                  "yet!")
