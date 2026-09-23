    @property
    def _rect_bbox(self):
        if self.drawtype == 'box':
            x, y = self.to_draw.center
            width = self.to_draw.width
            height = self.to_draw.height
            return x - width / 2., y - height / 2., width, height
        else:
            x, y = self.to_draw.get_data()
            x0, x1 = min(x), max(x)
            y0, y1 = min(y), max(y)
            return x0, y0, x1 - x0, y1 - y0
