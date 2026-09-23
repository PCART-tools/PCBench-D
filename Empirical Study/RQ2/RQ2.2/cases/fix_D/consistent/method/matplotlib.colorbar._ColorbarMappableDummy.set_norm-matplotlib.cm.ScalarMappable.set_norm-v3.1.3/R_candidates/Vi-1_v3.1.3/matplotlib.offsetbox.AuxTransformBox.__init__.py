    def __init__(self, aux_transform):
        self.aux_transform = aux_transform
        OffsetBox.__init__(self)

        self.offset_transform = mtransforms.Affine2D()
        self.offset_transform.clear()
        self.offset_transform.translate(0, 0)

        # ref_offset_transform is used to make the offset_transform is
        # always reference to the lower-left corner of the bbox of its
        # children.
        self.ref_offset_transform = mtransforms.Affine2D()
        self.ref_offset_transform.clear()
