    def byItem(self, data, itemindex=None, inplace=1):
        if itemindex is None:
            if inplace:
                data.sort()
                result = data
            else:
                result = sorted(data)
            return result
        else:
            aux = [(data[i][itemindex], i) for i in range(len(data))]
            return self._helper(data, aux, inplace)
