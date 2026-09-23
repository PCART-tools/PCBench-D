    def __init__(self, aux_transform):
        self.aux_transform = aux_transform
        OffsetBox.__init__(self)
        self.offset_transform = mtransforms.Affine2D()
        # ref_offset_transform makes offset_transform always relative to the
        # lower-left corner of the bbox of its children.
        self.ref_offset_transform = mtransforms.Affine2D()
