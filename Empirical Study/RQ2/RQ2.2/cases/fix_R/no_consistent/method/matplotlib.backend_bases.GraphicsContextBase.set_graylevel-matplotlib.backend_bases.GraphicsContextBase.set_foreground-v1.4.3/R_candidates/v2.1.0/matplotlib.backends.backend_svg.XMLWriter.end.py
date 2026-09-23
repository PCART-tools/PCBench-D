    def end(self, tag=None, indent=True):
        if tag:
            assert self.__tags, "unbalanced end(%s)" % tag
            assert escape_cdata(tag) == self.__tags[-1],\
                   "expected end(%s), got %s" % (self.__tags[-1], tag)
        else:
            assert self.__tags, "unbalanced end()"
        tag = self.__tags.pop()
        if self.__data:
            self.__flush(indent)
        elif self.__open:
            self.__open = 0
            self.__write("/>\n")
            return
        if indent:
            self.__write(self.__indentation[:len(self.__tags)])
        self.__write("</%s>\n" % tag)
