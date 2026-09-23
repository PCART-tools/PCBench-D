    def writeInfoDict(self):
        """Write out the info dictionary, checking it for good form"""

        self.infoObject = self.reserveObject('info')
        self.writeObject(self.infoObject, self.infoDict)
