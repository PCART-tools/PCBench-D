    @property
    def is_view(self) -> bool:
        """return a boolean if we are a single block and are a view"""
        if len(self.blocks) == 1:
            return self.blocks[0].is_view

        # It is technically possible to figure out which blocks are views
        # e.g. [ b.values.base is not None for b in self.blocks ]
        # but then we have the case of possibly some blocks being a view
        # and some blocks not. setting in theory is possible on the non-view
        # blocks w/o causing a SettingWithCopy raise/warn. But this is a bit
        # complicated

        return False
