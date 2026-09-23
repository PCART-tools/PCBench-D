    def get_active_marker(self):
        'get the active lineinestyle'
        ind = self.cbox_markers.get_active()
        m = self.markers[ind]
        return m
