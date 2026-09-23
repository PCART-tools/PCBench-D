@cbook.deprecated("3.0")
class ArrayWrapper:
    """Thin wrapper around numpy ndarray to expose the interface
       expected by cairocffi. Basically replicates the
       array.array interface.
    """
    def __init__(self, myarray):
        self.__array = myarray
        self.__data = myarray.ctypes.data
        self.__size = len(myarray.flatten())
        self.itemsize = myarray.itemsize

    def buffer_info(self):
        return (self.__data, self.__size)
