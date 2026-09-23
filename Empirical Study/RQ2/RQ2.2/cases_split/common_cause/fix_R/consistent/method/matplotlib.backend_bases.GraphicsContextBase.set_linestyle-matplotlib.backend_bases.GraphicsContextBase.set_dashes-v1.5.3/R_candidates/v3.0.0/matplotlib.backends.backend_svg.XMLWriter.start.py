    def start(self, tag, attrib={}, **extra):
        self.__flush()
        tag = escape_cdata(tag)
        self.__data = []
        self.__tags.append(tag)
        self.__write(self.__indentation[:len(self.__tags) - 1])
        self.__write("<%s" % tag)
        for k, v in sorted({**attrib, **extra}.items()):
            if not v == '':
                k = escape_cdata(k)
                v = escape_attrib(v)
                self.__write(" %s=\"%s\"" % (k, v))
        self.__open = 1
        return len(self.__tags)-1
