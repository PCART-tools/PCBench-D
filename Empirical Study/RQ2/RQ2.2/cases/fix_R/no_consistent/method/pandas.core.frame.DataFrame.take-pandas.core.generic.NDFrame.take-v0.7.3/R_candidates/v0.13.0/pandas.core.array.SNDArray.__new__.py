    def __new__(cls, data, index=None, name=None):
        data = data.view(SNDArray)
        data.index = index
        data.name = name

        return data
