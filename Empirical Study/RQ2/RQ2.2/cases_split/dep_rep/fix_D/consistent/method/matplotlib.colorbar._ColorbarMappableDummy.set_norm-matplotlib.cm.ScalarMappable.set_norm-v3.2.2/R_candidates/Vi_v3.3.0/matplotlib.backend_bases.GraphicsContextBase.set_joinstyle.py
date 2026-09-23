    def set_joinstyle(self, js):
        """Set the join style to be one of ('miter', 'round', 'bevel')."""
        cbook._check_in_list(['miter', 'round', 'bevel'], js=js)
        self._joinstyle = js
