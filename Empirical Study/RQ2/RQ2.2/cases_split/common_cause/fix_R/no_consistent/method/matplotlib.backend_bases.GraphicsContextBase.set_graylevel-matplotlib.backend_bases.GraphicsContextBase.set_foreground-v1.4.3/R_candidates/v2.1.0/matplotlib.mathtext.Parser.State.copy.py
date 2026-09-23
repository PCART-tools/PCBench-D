        def copy(self):
            return Parser.State(
                self.font_output,
                self.font,
                self.font_class,
                self.fontsize,
                self.dpi)
