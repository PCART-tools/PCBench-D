class MyArray(object):
    def __init__(self, x):
        self.x = x
        self.dtype = x.dtype
        self.shape = x.shape

    def __getitem__(self, i):
        return self.x[i]
