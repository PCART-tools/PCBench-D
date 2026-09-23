    def newTextnote(self, text, positionRect=[-100, -100, 0, 0]):
        # Create a new annotation of type text
        theNote = {'Type': Name('Annot'),
                   'Subtype': Name('Text'),
                   'Contents': text,
                   'Rect': positionRect,
                   }
        annotObject = self.reserveObject('annotation')
        self.writeObject(annotObject, theNote)
        self.pageAnnotations.append(annotObject)
