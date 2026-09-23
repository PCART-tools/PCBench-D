    def end(self, tag=None, indent=True):
        """
        Close the current element (opened by the most recent call to
        :meth:`start`).

        Parameters
        ----------
        tag
            Element tag.  If given, the tag must match the start tag.  If
            omitted, the current element is closed.
        indent : bool, default: True
        """
        if tag:
            assert self.__tags, f"unbalanced end({tag})"
            assert _escape_cdata(tag) == self.__tags[-1], \
                f"expected end({self.__tags[-1]}), got {tag}"
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
        self.__write(f"</{tag}>\n")
