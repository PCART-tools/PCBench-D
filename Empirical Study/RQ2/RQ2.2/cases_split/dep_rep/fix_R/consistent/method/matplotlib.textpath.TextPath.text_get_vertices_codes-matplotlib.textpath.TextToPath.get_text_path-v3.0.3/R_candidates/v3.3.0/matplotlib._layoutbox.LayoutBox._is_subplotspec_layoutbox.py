    def _is_subplotspec_layoutbox(self):
        """
        Helper to check if this layoutbox is the layoutbox of a subplotspec.
        """
        name = self.name.split('.')[-1]
        return name[:2] == 'ss'
