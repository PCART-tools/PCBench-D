    def get_joinstyle(self):
        return {'miter': 0, 'round': 1, 'bevel': 2}[
            GraphicsContextBase.get_joinstyle(self)]
