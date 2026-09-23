    def _get_label(self, label, axis=0):
        # ueber-hack
        if (isinstance(label, tuple) and
                isinstance(label[axis], slice)):

            raise IndexingError('no slices here')

        try:
            return self.obj._xs(label, axis=axis, copy=False)
        except Exception:
            return self.obj._xs(label, axis=axis, copy=True)
