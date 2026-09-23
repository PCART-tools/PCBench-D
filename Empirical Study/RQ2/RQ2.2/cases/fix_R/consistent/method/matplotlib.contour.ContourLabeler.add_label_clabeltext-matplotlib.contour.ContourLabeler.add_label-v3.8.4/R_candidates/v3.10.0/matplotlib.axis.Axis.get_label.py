    def get_label(self):
        """
        Return the axis label as a Text instance.

        .. admonition:: Discouraged

           This overrides `.Artist.get_label`, which is for legend labels, with a new
           semantic. It is recommended to use the attribute ``Axis.label`` instead.
        """
        return self.label
