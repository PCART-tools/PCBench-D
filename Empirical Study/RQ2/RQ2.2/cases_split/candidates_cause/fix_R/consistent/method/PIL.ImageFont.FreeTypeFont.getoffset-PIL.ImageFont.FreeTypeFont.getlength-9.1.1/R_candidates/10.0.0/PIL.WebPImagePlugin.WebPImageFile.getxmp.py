    def getxmp(self):
        """
        Returns a dictionary containing the XMP tags.
        Requires defusedxml to be installed.

        :returns: XMP tags in a dictionary.
        """
        return self._getxmp(self.info["xmp"]) if "xmp" in self.info else {}
