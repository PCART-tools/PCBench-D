    def is_empty(self):
        assert self.callbacks._func_cid_map == {}
        assert self.callbacks.callbacks == {}
