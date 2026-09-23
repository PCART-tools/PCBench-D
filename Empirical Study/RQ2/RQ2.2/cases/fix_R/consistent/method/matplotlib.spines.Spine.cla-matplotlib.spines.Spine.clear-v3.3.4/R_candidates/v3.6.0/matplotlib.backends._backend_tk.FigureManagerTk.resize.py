    def resize(self, width, height):
        max_size = 1_400_000  # the measured max on xorg 1.20.8 was 1_409_023

        if (width > max_size or height > max_size) and sys.platform == 'linux':
            raise ValueError(
                'You have requested to resize the '
                f'Tk window to ({width}, {height}), one of which '
                f'is bigger than {max_size}.  At larger sizes xorg will '
                'either exit with an error on newer versions (~1.20) or '
                'cause corruption on older version (~1.19).  We '
                'do not expect a window over a million pixel wide or tall '
                'to be intended behavior.')
        self.canvas._tkcanvas.configure(width=width, height=height)
