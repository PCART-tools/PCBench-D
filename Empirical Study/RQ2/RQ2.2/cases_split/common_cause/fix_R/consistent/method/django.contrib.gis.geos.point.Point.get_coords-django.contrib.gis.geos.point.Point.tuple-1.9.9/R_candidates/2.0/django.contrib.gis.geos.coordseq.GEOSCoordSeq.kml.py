    @property
    def kml(self):
        "Return the KML representation for the coordinates."
        # Getting the substitution string depending on whether the coordinates have
        #  a Z dimension.
        if self.hasz:
            substr = '%s,%s,%s '
        else:
            substr = '%s,%s,0 '
        return '<coordinates>%s</coordinates>' % \
            ''.join(substr % self[i] for i in range(len(self))).strip()
