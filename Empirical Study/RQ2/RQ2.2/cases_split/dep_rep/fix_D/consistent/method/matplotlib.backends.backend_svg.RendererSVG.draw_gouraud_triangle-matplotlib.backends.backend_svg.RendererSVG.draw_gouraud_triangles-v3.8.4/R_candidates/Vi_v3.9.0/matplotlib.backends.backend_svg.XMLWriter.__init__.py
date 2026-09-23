    def __init__(self, file):
        self.__write = file.write
        if hasattr(file, "flush"):
            self.flush = file.flush
        self.__open = 0  # true if start tag is open
        self.__tags = []
        self.__data = []
        self.__indentation = " " * 64
