    def __hash__(self):
        """
        override the hash function of any of the formatters, so that we don't
        create duplicate excel format styles
        """
        return hash(self.__class__)
