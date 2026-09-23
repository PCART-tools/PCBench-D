    def reserveObject(self, name=''):
        """Reserve an ID for an indirect object.
        The name is used for debugging in case we forget to print out
        the object with writeObject.
        """

        id = self.nextObject
        self.nextObject += 1
        self.xrefTable.append([None, 0, name])
        return Reference(id)
