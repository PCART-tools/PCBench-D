    @property
    def condition(self):
        if len(self.args) > 1:
            return self.args[1]
        else:
            return None
