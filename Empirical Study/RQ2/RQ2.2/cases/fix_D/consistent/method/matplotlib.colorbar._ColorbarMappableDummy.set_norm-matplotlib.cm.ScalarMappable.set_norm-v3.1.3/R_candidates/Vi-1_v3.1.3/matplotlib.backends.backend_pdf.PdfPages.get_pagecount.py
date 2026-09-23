    def get_pagecount(self):
        """
        Returns the current number of pages in the multipage pdf file.
        """
        return len(self._file.pageList)
