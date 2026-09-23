    def getxmp(self):
        """
        Returns a dictionary containing the XMP tags.
        Requires defusedxml to be installed.

        :returns: XMP tags in a dictionary.
        """
        return self._getxmp(self.tag_v2[XMP]) if XMP in self.tag_v2 else {}
