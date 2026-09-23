    def set_active(self, active):
        super().set_active(active)
        if active:
            self.update_background(None)
