    def on_mappable_changed(self, mappable):
        """
        Updates this colorbar to match the mappable's properties.

        Typically this is automatically registered as an event handler
        by :func:`colorbar_factory` and should not be called manually.

        """
        self.set_cmap(mappable.get_cmap())
        self.set_clim(mappable.get_clim())
        self.update_normal(mappable)
