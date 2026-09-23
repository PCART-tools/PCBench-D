    def count(self):
        count1 = sum(s == self.signal for s, p in self.callbacks._func_cid_map)
        count2 = len(self.callbacks.callbacks.get(self.signal))
        assert count1 == count2
        return count1
