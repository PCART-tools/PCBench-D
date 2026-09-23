    def _update(self):
        self.update_from(self.patch)

        # Place the shadow patch directly behind the inherited patch.
        self.set_zorder(np.nextafter(self.patch.zorder, -np.inf))

        self.update(self._props)
