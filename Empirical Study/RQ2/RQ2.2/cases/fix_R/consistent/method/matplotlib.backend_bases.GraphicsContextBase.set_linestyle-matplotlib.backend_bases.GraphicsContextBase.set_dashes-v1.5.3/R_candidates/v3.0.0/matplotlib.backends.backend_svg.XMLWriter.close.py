    def close(self, id):
        while len(self.__tags) > id:
            self.end()
