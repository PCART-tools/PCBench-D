        def open(self, im):
            im._mode = "RGB"
            self.bbox = im.info["wmf_bbox"]
