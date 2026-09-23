    def writeImages(self):
        for img, name, ob in six.itervalues(self._images):
            height, width, data, adata = self._unpack(img)
            if adata is not None:
                smaskObject = self.reserveObject("smask")
                self._writeImg(adata, height, width, True, smaskObject.id)
            else:
                smaskObject = None
            self._writeImg(data, height, width, False,
                           ob.id, smaskObject)
