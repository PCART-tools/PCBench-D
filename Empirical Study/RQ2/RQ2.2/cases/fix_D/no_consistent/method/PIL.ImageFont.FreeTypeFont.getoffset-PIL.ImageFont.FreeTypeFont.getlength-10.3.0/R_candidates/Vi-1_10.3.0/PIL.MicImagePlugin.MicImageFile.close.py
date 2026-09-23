    def close(self):
        self.__fp.close()
        self.ole.close()
        super().close()
