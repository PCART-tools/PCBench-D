    def get_text(self, lev, fmt):
        """Get the text of the label."""
        if isinstance(lev, str):
            return lev
        else:
            if isinstance(fmt, dict):
                return fmt.get(lev, '%1.3f')
            elif callable(fmt):
                return fmt(lev)
            else:
                return fmt % lev
