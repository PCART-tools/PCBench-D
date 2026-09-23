    def __init__(self, myarray):
        self.__array = myarray
        self.__data = myarray.ctypes.data
        self.__size = len(myarray.flatten())
        self.itemsize = myarray.itemsize
