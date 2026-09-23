    def connect(self, s, func, pickle):
        cid = self.callbacks.connect(s, func)
        if pickle:
            self.callbacks._pickled_cids.add(cid)
        return cid
