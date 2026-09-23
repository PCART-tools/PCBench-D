    def newPage(self, width, height):
        self.endStream()

        self.width, self.height = width, height
        contentObject = self.reserveObject('page contents')
        thePage = {'Type': Name('Page'),
                   'Parent': self.pagesObject,
                   'Resources': self.resourceObject,
                   'MediaBox': [0, 0, 72 * width, 72 * height],
                   'Contents': contentObject,
                   'Group': {'Type': Name('Group'),
                             'S': Name('Transparency'),
                             'CS': Name('DeviceRGB')},
                   'Annots': self.pageAnnotations,
                   }
        pageObject = self.reserveObject('page')
        self.writeObject(pageObject, thePage)
        self.pageList.append(pageObject)

        self.beginStream(contentObject.id,
                         self.reserveObject('length of content stream'))
        # Initialize the pdf graphics state to match the default mpl
        # graphics context: currently only the join style needs to be set
        self.output(GraphicsContextPdf.joinstyles['round'], Op.setlinejoin)

        # Clear the list of annotations for the next page
        self.pageAnnotations = []
