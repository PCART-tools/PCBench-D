        def __await__(self):
            return (yield from self.__iter__())
