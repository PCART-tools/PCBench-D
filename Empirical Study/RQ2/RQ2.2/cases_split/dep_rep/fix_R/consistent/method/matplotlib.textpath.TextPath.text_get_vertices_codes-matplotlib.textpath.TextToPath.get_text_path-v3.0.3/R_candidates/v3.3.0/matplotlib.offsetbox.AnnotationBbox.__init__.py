    @docstring.dedent_interpd
    def __init__(self, offsetbox, xy,
                 xybox=None,
                 xycoords='data',
                 boxcoords=None,
                 frameon=True, pad=0.4,  # FancyBboxPatch boxstyle.
                 annotation_clip=None,
                 box_alignment=(0.5, 0.5),
                 bboxprops=None,
                 arrowprops=None,
                 fontsize=None,
                 **kwargs):
        """
        Parameters
        ----------
        offsetbox : `OffsetBox`

        xy : (float, float)
            The point *(x, y)* to annotate. The coordinate system is determined
            by *xycoords*.

        xybox : (float, float), default: *xy*
            The position *(x, y)* to place the text at. The coordinate system
            is determined by *boxcoords*.

        xycoords : str or `.Artist` or `.Transform` or callable or \
(float, float), default: 'data'
            The coordinate system that *xy* is given in. See the parameter
            *xycoords* in `.Annotation` for a detailed description.

        boxcoords : str or `.Artist` or `.Transform` or callable or \
(float, float), default: value of *xycoords*
            The coordinate system that *xybox* is given in. See the parameter
            *textcoords* in `.Annotation` for a detailed description.

        frameon : bool, default: True
            Whether to draw a frame around the box.

        pad : float, default: 0.4
            Padding around the offsetbox.

        box_alignment : (float, float)
            A tuple of two floats for a vertical and horizontal alignment of
            the offset box w.r.t. the *boxcoords*.
            The lower-left corner is (0, 0) and upper-right corner is (1, 1).

        **kwargs
            Other parameters are identical to `.Annotation`.
        """

        martist.Artist.__init__(self, **kwargs)
        mtext._AnnotationBase.__init__(self,
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

        self._box_alignment = box_alignment

        # frame
        self.patch = FancyBboxPatch(
            xy=(0.0, 0.0), width=1., height=1.,
            facecolor='w', edgecolor='k',
            mutation_scale=self.prop.get_size_in_points(),
            snap=True,
            visible=frameon,
        )
        self.patch.set_boxstyle("square", pad=pad)
        if bboxprops:
            self.patch.set(**bboxprops)
