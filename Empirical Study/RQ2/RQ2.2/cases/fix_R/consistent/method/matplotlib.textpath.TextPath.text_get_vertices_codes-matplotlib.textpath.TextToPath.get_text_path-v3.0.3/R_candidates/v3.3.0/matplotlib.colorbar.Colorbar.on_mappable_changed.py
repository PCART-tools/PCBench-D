    @cbook.deprecated("3.3", alternative="update_normal")
    def on_mappable_changed(self, mappable):
        """
        Update this colorbar to match the mappable's properties.

        Typically this is automatically registered as an event handler
        by :func:`colorbar_factory` and should not be called manually.
        """
        _log.debug('colorbar mappable changed')
        self.update_normal(mappable)
