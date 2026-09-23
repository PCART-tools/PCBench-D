    def comment(self, comment):
        self.__flush()
        self.__write(self.__indentation[:len(self.__tags)])
        self.__write("<!-- %s -->\n" % escape_comment(comment))
