    def apply_broadcast(self):
        result = super().apply_broadcast(self.obj.T)
        return result.T
