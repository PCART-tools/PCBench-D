    def remove(self):
        super().remove()
        for text in self.labelTexts:
            text.remove()
