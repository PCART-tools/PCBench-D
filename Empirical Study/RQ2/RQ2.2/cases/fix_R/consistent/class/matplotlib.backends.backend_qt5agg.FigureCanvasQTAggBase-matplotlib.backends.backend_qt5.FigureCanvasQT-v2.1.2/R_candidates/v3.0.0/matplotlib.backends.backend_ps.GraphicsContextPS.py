class GraphicsContextPS(GraphicsContextBase):
    def get_capstyle(self):
        return {'butt':0,
                'round':1,
                'projecting':2}[GraphicsContextBase.get_capstyle(self)]

    def get_joinstyle(self):
        return {'miter':0,
                'round':1,
                'bevel':2}[GraphicsContextBase.get_joinstyle(self)]

    def shouldstroke(self):
        return (self.get_linewidth() > 0.0 and
                (len(self.get_rgb()) <= 3 or self.get_rgb()[3] != 0.0))
