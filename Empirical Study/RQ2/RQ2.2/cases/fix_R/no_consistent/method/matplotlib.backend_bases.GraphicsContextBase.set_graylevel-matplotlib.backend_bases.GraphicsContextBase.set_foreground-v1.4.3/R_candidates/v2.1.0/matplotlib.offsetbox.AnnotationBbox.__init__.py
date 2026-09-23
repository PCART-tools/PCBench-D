    @docstring.dedent_interpd
    def __init__(self, offsetbox, xy,
                 xybox=None,
                 xycoords='data',
                 boxcoords=None,
                 frameon=True, pad=0.4,  # BboxPatch
                 annotation_clip=None,
                 box_alignment=(0.5, 0.5),
                 bboxprops=None,
                 arrowprops=None,
                 fontsize=None,
                 **kwargs):
        """
        *offsetbox* : OffsetBox instance

        *xycoords* : same as Annotation but can be a tuple of two
           strings which are interpreted as x and y coordinates.

        *boxcoords* : similar to textcoords as Annotation but can be a
           tuple of two strings which are interpreted as x and y
           coordinates.

        *box_alignment* : a tuple of two floats for a vertical and
           horizontal alignment of the offset box w.r.t. the *boxcoords*.
           The lower-left corner is (0.0) and upper-right corner is (1.1).

        other parameters are identical to that of Annotation.
        """

        martist.Artist.__init__(self, **kwargs)
        _AnnotationBase.__init__(self,
                                 xy,
                                 xycoords=xycoords,
                                 annotation_clip=annotation_clip)

        self.offsetbox = offsetbox

        self.arrowprops = arrowprops

        self.set_fontsize(fontsize)

        if xybox is None:
            self.xybox = xy
        else:
            self.xybox = xybox

        if boxcoords is None:
            self.boxcoords = xycoords
        else:
            self.boxcoords = boxcoords

        if arrowprops is not None:
            self._arrow_relpos = self.arrowprops.pop("relpos", (0.5, 0.5))
            self.arrow_patch = FancyArrowPatch((0, 0), (1, 1),
                                               **self.arrowprops)
        else:
            self._arrow_relpos = None
            self.arrow_patch = None

        #self._fw, self._fh = 0., 0. # for alignment
        self._box_alignment = box_alignment

        # frame
        self.patch = FancyBboxPatch(
            xy=(0.0, 0.0), width=1., height=1.,
            facecolor='w', edgecolor='k',
            mutation_scale=self.prop.get_size_in_points(),
            snap=True
            )
        self.patch.set_boxstyle("square", pad=pad)
        if bboxprops:
            self.patch.set(**bboxprops)
        self._drawFrame = frameon
