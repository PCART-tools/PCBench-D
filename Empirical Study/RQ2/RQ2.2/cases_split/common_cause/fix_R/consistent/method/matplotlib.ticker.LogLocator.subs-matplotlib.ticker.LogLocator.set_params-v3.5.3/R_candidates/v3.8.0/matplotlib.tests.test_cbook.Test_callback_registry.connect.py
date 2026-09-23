    def connect(self, s, func, pickle):
        if pickle:
            return self.callbacks.connect(s, func)
        else:
            return self.callbacks._connect_picklable(s, func)
