    def get_joinstyle(self):
        return {'miter': 0, 'round': 1, 'bevel': 2}[super().get_joinstyle()]
