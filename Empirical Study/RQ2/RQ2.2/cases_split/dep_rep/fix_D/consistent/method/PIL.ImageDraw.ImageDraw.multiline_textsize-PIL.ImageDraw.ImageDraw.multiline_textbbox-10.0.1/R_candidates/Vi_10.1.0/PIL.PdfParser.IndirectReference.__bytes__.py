    def __bytes__(self):
        return self.__str__().encode("us-ascii")
