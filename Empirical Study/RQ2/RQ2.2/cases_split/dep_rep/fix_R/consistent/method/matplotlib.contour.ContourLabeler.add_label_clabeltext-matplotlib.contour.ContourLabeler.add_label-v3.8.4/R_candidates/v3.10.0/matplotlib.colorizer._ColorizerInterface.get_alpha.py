    def get_alpha(self):
        try:
            return super().get_alpha()
        except AttributeError:
            return 1
