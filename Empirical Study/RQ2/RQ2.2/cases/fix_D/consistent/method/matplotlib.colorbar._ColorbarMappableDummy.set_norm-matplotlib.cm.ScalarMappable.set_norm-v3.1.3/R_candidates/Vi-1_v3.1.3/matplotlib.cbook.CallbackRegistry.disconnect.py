    def disconnect(self, cid):
        """Disconnect the callback registered with callback id *cid*.
        """
        for eventname, callbackd in list(self.callbacks.items()):
            try:
                del callbackd[cid]
            except KeyError:
                continue
            else:
                for signal, functions in list(self._func_cid_map.items()):
                    for function, value in list(functions.items()):
                        if value == cid:
                            del functions[function]
                return
