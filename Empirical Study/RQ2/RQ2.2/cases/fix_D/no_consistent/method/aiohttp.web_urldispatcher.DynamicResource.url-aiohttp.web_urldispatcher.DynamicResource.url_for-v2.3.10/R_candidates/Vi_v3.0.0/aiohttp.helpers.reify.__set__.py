    def __set__(self, inst, value):
        raise AttributeError("reified property is read-only")
