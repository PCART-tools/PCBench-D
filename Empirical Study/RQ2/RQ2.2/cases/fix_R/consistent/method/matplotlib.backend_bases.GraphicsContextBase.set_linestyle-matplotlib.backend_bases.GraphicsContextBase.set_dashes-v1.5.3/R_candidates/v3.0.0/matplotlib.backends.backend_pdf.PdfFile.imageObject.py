    def imageObject(self, image):
        """Return name of an image XObject representing the given image."""

        entry = self._images.get(id(image), None)
        if entry is not None:
            return entry[1]

        name = Name('I%d' % self.nextImage)
        ob = self.reserveObject('image %d' % self.nextImage)
        self.nextImage += 1
        self._images[id(image)] = (image, name, ob)
        return name
