    def __getstate__(self):
        # turn the dictionary with weak values into a normal dictionary
        return {**self.__dict__,
                '_parents': {k: v() for k, v in self._parents.items()}}
