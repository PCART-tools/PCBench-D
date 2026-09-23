    def get_pagecount(self):
        """Return the current number of pages in the multipage pdf file."""
        return len(self._file.pageList)
