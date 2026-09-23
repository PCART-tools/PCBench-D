        def load(self, data):
            res = super().load(data)
            return res.replace(tzinfo=self.timezone)
