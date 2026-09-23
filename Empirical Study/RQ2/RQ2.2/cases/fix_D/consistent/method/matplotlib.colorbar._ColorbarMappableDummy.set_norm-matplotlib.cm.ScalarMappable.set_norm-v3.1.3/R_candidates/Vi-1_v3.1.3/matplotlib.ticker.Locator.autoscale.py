    def autoscale(self):
        """autoscale the view limits"""
        return self.view_limits(*self.axis.get_view_interval())
