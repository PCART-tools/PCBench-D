        def open(self, im):
            im.mode = "RGB"
            self.bbox = im.info["wmf_bbox"]
