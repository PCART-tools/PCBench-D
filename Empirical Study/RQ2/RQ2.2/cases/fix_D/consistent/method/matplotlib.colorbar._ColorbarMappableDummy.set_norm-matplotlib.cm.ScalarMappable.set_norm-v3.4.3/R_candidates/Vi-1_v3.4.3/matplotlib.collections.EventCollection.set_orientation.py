    def set_orientation(self, orientation=None):
        """
        Set the orientation of the event line.

        Parameters
        ----------
        orientation : {'horizontal', 'vertical'}
        """
        try:
            is_horizontal = _api.check_getitem(
                {"horizontal": True, "vertical": False},
                orientation=orientation)
        except ValueError:
            if (orientation is None or orientation.lower() == "none"
                    or orientation.lower() == "horizontal"):
                is_horizontal = True
            elif orientation.lower() == "vertical":
                is_horizontal = False
            else:
                raise
            normalized = "horizontal" if is_horizontal else "vertical"
            _api.warn_deprecated(
                "3.3", message="Support for setting the orientation of "
                f"EventCollection to {orientation!r} is deprecated since "
                f"%(since)s and will be removed %(removal)s; please set it to "
                f"{normalized!r} instead.")
        if is_horizontal == self.is_horizontal():
            return
        self.switch_orientation()
