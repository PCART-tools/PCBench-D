    @_api.deprecated("3.4")
    def destroy(self):
        """
        Fix any cyclical references before the object is about
        to be destroyed.
        """
        self.used_characters = None
