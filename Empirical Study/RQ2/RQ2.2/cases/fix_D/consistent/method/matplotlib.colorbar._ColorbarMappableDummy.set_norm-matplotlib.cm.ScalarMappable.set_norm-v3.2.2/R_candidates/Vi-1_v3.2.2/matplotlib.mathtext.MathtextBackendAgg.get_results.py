    def get_results(self, box, used_characters):
        self.mode = 'bbox'
        orig_height = box.height
        orig_depth  = box.depth
        ship(0, 0, box)
        bbox = self.bbox
        bbox = [bbox[0] - 1, bbox[1] - 1, bbox[2] + 1, bbox[3] + 1]
        self.mode = 'render'
        self.set_canvas_size(
            bbox[2] - bbox[0],
            (bbox[3] - bbox[1]) - orig_depth,
            (bbox[3] - bbox[1]) - orig_height)
        ship(-bbox[0], -bbox[1], box)
        result = (self.ox,
                  self.oy,
                  self.width,
                  self.height + self.depth,
                  self.depth,
                  self.image,
                  used_characters)
        self.image = None
        return result
