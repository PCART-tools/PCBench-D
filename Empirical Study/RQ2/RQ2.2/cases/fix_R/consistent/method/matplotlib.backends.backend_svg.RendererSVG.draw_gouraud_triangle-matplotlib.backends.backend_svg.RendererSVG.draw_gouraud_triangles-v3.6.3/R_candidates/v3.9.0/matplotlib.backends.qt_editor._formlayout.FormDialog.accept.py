    def accept(self):
        self.data = self.formwidget.get()
        self.apply_callback(self.data)
        super().accept()
