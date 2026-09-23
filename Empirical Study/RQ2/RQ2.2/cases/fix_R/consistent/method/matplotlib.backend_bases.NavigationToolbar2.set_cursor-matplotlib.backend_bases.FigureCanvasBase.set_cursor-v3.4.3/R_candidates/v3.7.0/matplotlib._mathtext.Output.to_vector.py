    def to_vector(self):
        w, h, d = map(
            np.ceil, [self.box.width, self.box.height, self.box.depth])
        gs = [(info.font, info.fontsize, info.num, ox, h - oy + info.offset)
              for ox, oy, info in self.glyphs]
        rs = [(x1, h - y2, x2 - x1, y2 - y1)
              for x1, y1, x2, y2 in self.rects]
        return VectorParse(w, h + d, d, gs, rs)
