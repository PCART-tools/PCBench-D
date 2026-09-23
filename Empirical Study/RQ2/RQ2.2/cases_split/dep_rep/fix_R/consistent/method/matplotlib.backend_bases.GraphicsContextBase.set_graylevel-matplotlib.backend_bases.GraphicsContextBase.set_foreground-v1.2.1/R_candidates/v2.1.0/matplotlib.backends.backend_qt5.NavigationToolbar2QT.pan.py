    def pan(self, *args):
        super(NavigationToolbar2QT, self).pan(*args)
        self._update_buttons_checked()
