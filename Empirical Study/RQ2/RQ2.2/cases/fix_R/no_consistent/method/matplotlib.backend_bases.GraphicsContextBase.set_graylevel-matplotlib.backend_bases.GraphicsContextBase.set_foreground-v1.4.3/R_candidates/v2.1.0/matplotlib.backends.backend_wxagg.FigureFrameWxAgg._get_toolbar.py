    def _get_toolbar(self, statbar):
        if matplotlib.rcParams['toolbar'] == 'toolbar2':
            toolbar = NavigationToolbar2WxAgg(self.canvas)
            toolbar.set_status_bar(statbar)
        else:
            toolbar = None
        return toolbar
