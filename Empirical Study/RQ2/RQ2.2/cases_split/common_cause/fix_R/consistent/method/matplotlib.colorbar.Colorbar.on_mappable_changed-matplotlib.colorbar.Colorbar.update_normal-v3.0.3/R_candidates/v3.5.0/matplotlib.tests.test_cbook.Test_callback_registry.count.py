    def count(self):
        count1 = len(self.callbacks._func_cid_map.get(self.signal, []))
        count2 = len(self.callbacks.callbacks.get(self.signal))
        assert count1 == count2
        return count1
