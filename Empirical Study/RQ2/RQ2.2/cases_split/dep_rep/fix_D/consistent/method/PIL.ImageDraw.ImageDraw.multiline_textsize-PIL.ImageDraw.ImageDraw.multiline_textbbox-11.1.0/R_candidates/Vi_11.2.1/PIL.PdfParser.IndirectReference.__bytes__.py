    def __bytes__(self) -> bytes:
        return self.__str__().encode("us-ascii")
