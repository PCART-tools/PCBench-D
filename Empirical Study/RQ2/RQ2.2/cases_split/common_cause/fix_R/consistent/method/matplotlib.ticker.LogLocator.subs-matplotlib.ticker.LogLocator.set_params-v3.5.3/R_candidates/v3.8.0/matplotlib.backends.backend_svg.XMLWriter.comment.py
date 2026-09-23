    def comment(self, comment):
        """
        Add a comment to the output stream.

        Parameters
        ----------
        comment : str
            Comment text.
        """
        self.__flush()
        self.__write(self.__indentation[:len(self.__tags)])
        self.__write(f"<!-- {_escape_comment(comment)} -->\n")
