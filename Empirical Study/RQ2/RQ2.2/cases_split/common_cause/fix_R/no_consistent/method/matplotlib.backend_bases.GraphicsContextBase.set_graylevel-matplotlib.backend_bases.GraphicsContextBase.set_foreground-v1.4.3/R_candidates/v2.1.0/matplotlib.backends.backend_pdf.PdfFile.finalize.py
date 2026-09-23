    def finalize(self):
        "Write out the various deferred objects and the pdf end matter."

        self.endStream()
        self.writeFonts()
        self.writeObject(
            self.alphaStateObject,
            {val[0]: val[1] for val in six.itervalues(self.alphaStates)})
        self.writeHatches()
        self.writeGouraudTriangles()
        xobjects = {
            name: ob for image, name, ob in six.itervalues(self._images)}
        for tup in six.itervalues(self.markers):
            xobjects[tup[0]] = tup[1]
        for name, value in six.iteritems(self.multi_byte_charprocs):
            xobjects[name] = value
        for name, path, trans, ob, join, cap, padding, filled, stroked \
                in self.paths:
            xobjects[name] = ob
        self.writeObject(self.XObjectObject, xobjects)
        self.writeImages()
        self.writeMarkers()
        self.writePathCollectionTemplates()
        self.writeObject(self.pagesObject,
                         {'Type': Name('Pages'),
                          'Kids': self.pageList,
                          'Count': len(self.pageList)})
        self.writeInfoDict()

        # Finalize the file
        self.writeXref()
        self.writeTrailer()
