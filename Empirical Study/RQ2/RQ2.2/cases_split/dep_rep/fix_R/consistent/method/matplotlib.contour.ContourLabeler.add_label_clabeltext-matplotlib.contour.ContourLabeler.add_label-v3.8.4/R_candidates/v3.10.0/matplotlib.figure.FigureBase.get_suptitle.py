    def get_suptitle(self):
        """Return the suptitle as string or an empty string if not set."""
        text_obj = self._suptitle
        return "" if text_obj is None else text_obj.get_text()
