    def _helper(self, data, aux, inplace):
        aux.sort()
        result = [data[i] for junk, i in aux]
        if inplace:
            data[:] = result
        return result
