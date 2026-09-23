    def __copy__(self):
        cls = self.__class__
        cmapobject = cls.__new__(cls)
        cmapobject.__dict__.update(self.__dict__)

        cmapobject._rgba_outside = np.copy(self._rgba_outside)
        cmapobject._rgba_bad = np.copy(self._rgba_bad)
        cmapobject._shape = self.shape
        if self._isinit:
            cmapobject._lut = np.copy(self._lut)
        return cmapobject
