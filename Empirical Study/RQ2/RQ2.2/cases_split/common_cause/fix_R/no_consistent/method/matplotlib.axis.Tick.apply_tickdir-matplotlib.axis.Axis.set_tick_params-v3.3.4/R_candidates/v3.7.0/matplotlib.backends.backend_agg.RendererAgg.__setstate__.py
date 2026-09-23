    def __setstate__(self, state):
        self.__init__(state['width'], state['height'], state['dpi'])
