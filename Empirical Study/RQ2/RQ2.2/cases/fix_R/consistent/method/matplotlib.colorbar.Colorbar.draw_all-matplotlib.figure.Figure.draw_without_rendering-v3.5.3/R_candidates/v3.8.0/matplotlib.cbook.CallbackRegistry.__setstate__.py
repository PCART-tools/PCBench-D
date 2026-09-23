    def __setstate__(self, state):
        cid_count = state.pop('_cid_gen')
        vars(self).update(state)
        self.callbacks = {
            s: {cid: _weak_or_strong_ref(func, self._remove_proxy)
                for cid, func in d.items()}
            for s, d in self.callbacks.items()}
        self._func_cid_map = {
            s: {proxy: cid for cid, proxy in d.items()}
            for s, d in self.callbacks.items()}
        self._cid_gen = itertools.count(cid_count)
