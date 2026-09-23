@_api.deprecated("3.4", alternative="GraphicsContextBase")
class GraphicsContextPS(GraphicsContextBase):
    def get_capstyle(self):
        return {'butt': 0, 'round': 1, 'projecting': 2}[super().get_capstyle()]

    def get_joinstyle(self):
        return {'miter': 0, 'round': 1, 'bevel': 2}[super().get_joinstyle()]
