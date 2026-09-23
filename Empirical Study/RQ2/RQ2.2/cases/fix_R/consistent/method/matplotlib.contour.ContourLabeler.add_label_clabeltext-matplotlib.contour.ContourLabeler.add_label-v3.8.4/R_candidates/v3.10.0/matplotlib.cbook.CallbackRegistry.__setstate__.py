    def __setstate__(self, state):
        cid_count = state.pop('_cid_gen')
        vars(self).update(state)
        self.callbacks = {
            s: {cid: _weak_or_strong_ref(func, functools.partial(self._remove_proxy, s))
                for cid, func in d.items()}
            for s, d in self.callbacks.items()}
        self._func_cid_map = _UnhashDict(
            ((s, proxy), cid)
            for s, d in self.callbacks.items() for cid, proxy in d.items())
        self._cid_gen = itertools.count(cid_count)
