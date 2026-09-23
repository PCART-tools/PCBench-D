    def tostring_rgba_minimized(self):
        extents = self.get_content_extents()
        bbox = [[extents[0], self.height - (extents[1] + extents[3])],
                [extents[0] + extents[2], self.height - extents[1]]]
        region = self.copy_from_bbox(bbox)
        return np.array(region), extents
