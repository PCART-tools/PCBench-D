    @_api.deprecated("3.4")
    def destroy(self):
        self.glyphd = None
        super().destroy()
