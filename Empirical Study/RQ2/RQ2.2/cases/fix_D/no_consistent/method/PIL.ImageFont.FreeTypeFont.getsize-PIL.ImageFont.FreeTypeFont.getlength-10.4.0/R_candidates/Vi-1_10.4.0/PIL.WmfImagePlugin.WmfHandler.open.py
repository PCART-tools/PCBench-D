        def open(self, im: ImageFile.StubImageFile) -> None:
            im._mode = "RGB"
            self.bbox = im.info["wmf_bbox"]
