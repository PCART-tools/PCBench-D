    @vcenter.setter
    def vcenter(self, vcenter):
        if vcenter != self._vcenter:
            self._vcenter = vcenter
            # Trigger an update of the vmin/vmax values through the setter
            self.halfrange = self.halfrange
            self._changed()
