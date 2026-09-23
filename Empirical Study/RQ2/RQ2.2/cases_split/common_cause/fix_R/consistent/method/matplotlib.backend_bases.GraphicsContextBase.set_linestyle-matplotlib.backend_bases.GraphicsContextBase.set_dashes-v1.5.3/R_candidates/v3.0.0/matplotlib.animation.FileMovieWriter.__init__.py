    def __init__(self, *args, **kwargs):
        MovieWriter.__init__(self, *args, **kwargs)
        self.frame_format = rcParams['animation.frame_format']
