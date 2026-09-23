    def byAttribute(self, data, attributename, inplace=1):
        aux = [(getattr(data[i], attributename), i) for i in range(len(data))]
        return self._helper(data, aux, inplace)
