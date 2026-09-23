    def compress(self, condition, axis=0, out=None, **kwargs):
        # 1-d compat with numpy
        return self[condition]
