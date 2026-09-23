    def _post_process_cython_aggregate(self, obj):
        # undoing kludge from below
        if self.axis == 0:
            obj = obj.swapaxes(0, 1)
        return obj
