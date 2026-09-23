    def __getstate__(self):
        return {**self.__dict__, "_layoutbox": None}
