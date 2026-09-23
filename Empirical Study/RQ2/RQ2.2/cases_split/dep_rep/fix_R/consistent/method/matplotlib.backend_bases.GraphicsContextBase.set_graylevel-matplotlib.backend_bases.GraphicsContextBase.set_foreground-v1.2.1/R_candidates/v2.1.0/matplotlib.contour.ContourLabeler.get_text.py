    def get_text(self, lev, fmt):
        "get the text of the label"
        if isinstance(lev, six.string_types):
            return lev
        else:
            if isinstance(fmt, dict):
                return fmt[lev]
            elif callable(fmt):
                return fmt(lev)
            else:
                return fmt % lev
