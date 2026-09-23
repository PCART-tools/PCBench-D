    def get_tightbbox(self, renderer):
        # docstring inherited
        bboxes = [child.get_tightbbox(renderer)
                  for child in self.get_children()]

        return Bbox.union(bboxes)
