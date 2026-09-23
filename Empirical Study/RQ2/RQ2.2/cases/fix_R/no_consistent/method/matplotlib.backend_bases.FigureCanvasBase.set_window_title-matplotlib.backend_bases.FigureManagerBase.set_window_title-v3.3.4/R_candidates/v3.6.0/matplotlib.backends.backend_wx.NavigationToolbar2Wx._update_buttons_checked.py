    def _update_buttons_checked(self):
        if "Pan" in self.wx_ids:
            self.ToggleTool(self.wx_ids["Pan"], self.mode.name == "PAN")
        if "Zoom" in self.wx_ids:
            self.ToggleTool(self.wx_ids["Zoom"], self.mode.name == "ZOOM")
