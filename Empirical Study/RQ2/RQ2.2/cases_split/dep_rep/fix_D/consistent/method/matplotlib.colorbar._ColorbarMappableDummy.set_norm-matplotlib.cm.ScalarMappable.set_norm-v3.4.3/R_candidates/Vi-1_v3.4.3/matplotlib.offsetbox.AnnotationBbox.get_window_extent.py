    def get_window_extent(self, renderer):
        """
        get the bounding box in display space.
        """
        bboxes = [child.get_window_extent(renderer)
                  for child in self.get_children()]

        return Bbox.union(bboxes)
