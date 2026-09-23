    def writeImages(self):
        for img, name, ob in self._images.values():
            height, width, data, adata = self._unpack(img)
            if adata is not None:
                smaskObject = self.reserveObject("smask")
                self._writeImg(adata, height, width, True, smaskObject.id)
            else:
                smaskObject = None
            self._writeImg(data, height, width, False,
                           ob.id, smaskObject)
