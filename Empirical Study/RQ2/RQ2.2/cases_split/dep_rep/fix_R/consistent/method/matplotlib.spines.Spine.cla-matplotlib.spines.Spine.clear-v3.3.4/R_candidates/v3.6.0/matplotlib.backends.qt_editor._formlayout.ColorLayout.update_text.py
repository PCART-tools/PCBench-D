    def update_text(self, color):
        self.lineedit.setText(mcolors.to_hex(color.getRgbF(), keep_alpha=True))
