    def is_not_empty(self):
        np.testing.break_cycles()
        assert [*self.callbacks._func_cid_map] != []
        assert self.callbacks.callbacks != {}
