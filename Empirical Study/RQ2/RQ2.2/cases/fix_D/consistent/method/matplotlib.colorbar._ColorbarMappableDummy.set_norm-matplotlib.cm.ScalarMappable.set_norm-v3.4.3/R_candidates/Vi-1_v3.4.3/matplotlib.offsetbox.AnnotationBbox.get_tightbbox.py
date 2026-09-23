    def get_tightbbox(self, renderer):
        """
        get tight bounding box in display space.
        """
        bboxes = [child.get_tightbbox(renderer)
                  for child in self.get_children()]

        return Bbox.union(bboxes)
