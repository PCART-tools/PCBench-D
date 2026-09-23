    def __copy__(self):
        cls = self.__class__
        cmapobject = cls.__new__(cls)
        cmapobject.__dict__.update(self.__dict__)
        cmapobject._colormaps = [cm.copy() for cm in self._colormaps]
        cmapobject._rgba_bad = np.copy(self._rgba_bad)
        return cmapobject
