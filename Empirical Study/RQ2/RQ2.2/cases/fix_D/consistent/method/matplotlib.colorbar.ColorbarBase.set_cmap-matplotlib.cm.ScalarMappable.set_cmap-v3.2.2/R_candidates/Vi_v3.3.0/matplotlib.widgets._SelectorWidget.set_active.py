    def set_active(self, active):
        AxesWidget.set_active(self, active)
        if active:
            self.update_background(None)
