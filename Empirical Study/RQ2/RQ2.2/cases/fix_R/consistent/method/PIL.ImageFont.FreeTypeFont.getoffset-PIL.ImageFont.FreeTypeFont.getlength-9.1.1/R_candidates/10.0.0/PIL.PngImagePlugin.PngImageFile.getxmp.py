    def getxmp(self):
        """
        Returns a dictionary containing the XMP tags.
        Requires defusedxml to be installed.

        :returns: XMP tags in a dictionary.
        """
        return (
            self._getxmp(self.info["XML:com.adobe.xmp"])
            if "XML:com.adobe.xmp" in self.info
            else {}
        )
