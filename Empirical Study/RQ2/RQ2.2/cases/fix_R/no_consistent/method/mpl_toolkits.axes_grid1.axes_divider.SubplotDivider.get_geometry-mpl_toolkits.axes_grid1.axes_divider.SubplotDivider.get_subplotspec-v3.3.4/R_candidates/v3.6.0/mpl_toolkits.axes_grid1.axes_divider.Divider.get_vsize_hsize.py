    @_api.deprecated("3.5")
    def get_vsize_hsize(self):
        vsize = Size.AddList(self.get_vertical())
        hsize = Size.AddList(self.get_horizontal())
        return vsize, hsize
