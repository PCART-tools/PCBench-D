    def writeObject(self, object, contents):
        self.recordXref(object.id)
        object.write(contents, self)
