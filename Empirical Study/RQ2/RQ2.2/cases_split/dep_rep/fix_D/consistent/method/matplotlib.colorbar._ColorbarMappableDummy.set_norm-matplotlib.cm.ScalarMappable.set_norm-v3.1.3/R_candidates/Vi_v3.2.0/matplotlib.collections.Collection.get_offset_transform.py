    def get_offset_transform(self):
        t = self._transOffset
        if (not isinstance(t, transforms.Transform)
                and hasattr(t, '_as_mpl_transform')):
            t = t._as_mpl_transform(self.axes)
        return t
