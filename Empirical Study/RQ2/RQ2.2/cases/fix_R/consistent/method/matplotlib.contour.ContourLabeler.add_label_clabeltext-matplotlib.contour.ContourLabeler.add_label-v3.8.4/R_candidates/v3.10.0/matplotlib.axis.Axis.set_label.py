    def set_label(self, s):
        """Assigning legend labels is not supported. Raises RuntimeError."""
        raise RuntimeError(
            "A legend label cannot be assigned to an Axis. Did you mean to "
            "set the axis label via set_label_text()?")
