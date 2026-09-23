    @cbook.deprecated("3.2")
    def autoscale(self):
        """Autoscale the view limits."""
        return self.view_limits(*self.axis.get_view_interval())
