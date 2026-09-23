    def apply_broadcast(self):
        result = super(FrameColumnApply, self).apply_broadcast(self.obj.T)
        return result.T
