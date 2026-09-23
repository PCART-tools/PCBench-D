    def get_window_extent(self, renderer):
        # docstring inherited
        bboxes = [child.get_window_extent(renderer)
                  for child in self.get_children()]

        return Bbox.union(bboxes)
