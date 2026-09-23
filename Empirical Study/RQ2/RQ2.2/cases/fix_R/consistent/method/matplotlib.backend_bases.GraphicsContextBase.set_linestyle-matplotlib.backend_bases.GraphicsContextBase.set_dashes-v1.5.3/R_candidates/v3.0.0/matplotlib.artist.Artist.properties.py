    def properties(self):
        """
        return a dictionary mapping property name -> value for all Artist props
        """
        return ArtistInspector(self).properties()
