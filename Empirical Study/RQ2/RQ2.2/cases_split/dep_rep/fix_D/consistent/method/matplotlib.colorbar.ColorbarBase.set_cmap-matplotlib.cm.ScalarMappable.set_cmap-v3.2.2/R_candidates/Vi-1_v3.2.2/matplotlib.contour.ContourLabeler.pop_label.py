    def pop_label(self, index=-1):
        """Defaults to removing last label, but any index can be supplied"""
        self.labelCValues.pop(index)
        t = self.labelTexts.pop(index)
        t.remove()
