    def __init__(self, ref_artist, offsetbox, use_blit=False):
        DraggableBase.__init__(self, ref_artist, use_blit=use_blit)
        self.offsetbox = offsetbox
