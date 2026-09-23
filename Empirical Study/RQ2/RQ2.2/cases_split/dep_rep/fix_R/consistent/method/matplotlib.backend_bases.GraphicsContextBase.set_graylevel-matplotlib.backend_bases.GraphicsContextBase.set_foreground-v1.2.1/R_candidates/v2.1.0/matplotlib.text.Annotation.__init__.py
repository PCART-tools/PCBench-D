    @docstring.dedent_interpd
    def __init__(self, s, xy,
                 xytext=None,
                 xycoords='data',
                 textcoords=None,
                 arrowprops=None,
                 annotation_clip=None,
                 **kwargs):
        '''
        Annotate the point ``xy`` with text ``s``.

        Additional kwargs are passed to `~matplotlib.text.Text`.

        Parameters
        ----------

        s : str
            The text of the annotation

        xy : iterable
            Length 2 sequence specifying the *(x,y)* point to annotate

        xytext : iterable, optional
            Length 2 sequence specifying the *(x,y)* to place the text
            at.  If None, defaults to ``xy``.

        xycoords : str, Artist, Transform, callable or tuple, optional

            The coordinate system that ``xy`` is given in.

            For a `str` the allowed values are:

            =================   ===============================================
            Property            Description
            =================   ===============================================
            'figure points'     points from the lower left of the figure
            'figure pixels'     pixels from the lower left of the figure
            'figure fraction'   fraction of figure from lower left
            'axes points'       points from lower left corner of axes
            'axes pixels'       pixels from lower left corner of axes
            'axes fraction'     fraction of axes from lower left
            'data'              use the coordinate system of the object being
                                annotated (default)
            'polar'             *(theta,r)* if not native 'data' coordinates
            =================   ===============================================

            If a `~matplotlib.artist.Artist` object is passed in the units are
            fraction if it's bounding box.

            If a `~matplotlib.transforms.Transform` object is passed
            in use that to transform ``xy`` to screen coordinates

            If a callable it must take a
            `~matplotlib.backend_bases.RendererBase` object as input
            and return a `~matplotlib.transforms.Transform` or
            `~matplotlib.transforms.Bbox` object

            If a `tuple` must be length 2 tuple of str, `Artist`,
            `Transform` or callable objects.  The first transform is
            used for the *x* coordinate and the second for *y*.

            See :ref:`plotting-guide-annotation` for more details.

            Defaults to ``'data'``

        textcoords : str, `Artist`, `Transform`, callable or tuple, optional
            The coordinate system that ``xytext`` is given, which
            may be different than the coordinate system used for
            ``xy``.

            All ``xycoords`` values are valid as well as the following
            strings:

            =================   =========================================
            Property            Description
            =================   =========================================
            'offset points'     offset (in points) from the *xy* value
            'offset pixels'     offset (in pixels) from the *xy* value
            =================   =========================================

            defaults to the input of ``xycoords``

        arrowprops : dict, optional
            If not None, properties used to draw a
            `~matplotlib.patches.FancyArrowPatch` arrow between ``xy`` and
            ``xytext``.

            If `arrowprops` does not contain the key ``'arrowstyle'`` the
            allowed keys are:

            ==========   ======================================================
            Key          Description
            ==========   ======================================================
            width        the width of the arrow in points
            headwidth    the width of the base of the arrow head in points
            headlength   the length of the arrow head in points
            shrink       fraction of total length to 'shrink' from both ends
            ?            any key to :class:`matplotlib.patches.FancyArrowPatch`
            ==========   ======================================================

            If the `arrowprops` contains the key ``'arrowstyle'`` the
            above keys are forbidden.  The allowed values of
            ``'arrowstyle'`` are:

            ============   =============================================
            Name           Attrs
            ============   =============================================
            ``'-'``        None
            ``'->'``       head_length=0.4,head_width=0.2
            ``'-['``       widthB=1.0,lengthB=0.2,angleB=None
            ``'|-|'``      widthA=1.0,widthB=1.0
            ``'-|>'``      head_length=0.4,head_width=0.2
            ``'<-'``       head_length=0.4,head_width=0.2
            ``'<->'``      head_length=0.4,head_width=0.2
            ``'<|-'``      head_length=0.4,head_width=0.2
            ``'<|-|>'``    head_length=0.4,head_width=0.2
            ``'fancy'``    head_length=0.4,head_width=0.4,tail_width=0.4
            ``'simple'``   head_length=0.5,head_width=0.5,tail_width=0.2
            ``'wedge'``    tail_width=0.3,shrink_factor=0.5
            ============   =============================================

            Valid keys for `~matplotlib.patches.FancyArrowPatch` are:

            ===============  ==================================================
            Key              Description
            ===============  ==================================================
            arrowstyle       the arrow style
            connectionstyle  the connection style
            relpos           default is (0.5, 0.5)
            patchA           default is bounding box of the text
            patchB           default is None
            shrinkA          default is 2 points
            shrinkB          default is 2 points
            mutation_scale   default is text size (in points)
            mutation_aspect  default is 1.
            ?                any key for :class:`matplotlib.patches.PathPatch`
            ===============  ==================================================

            Defaults to None

        annotation_clip : bool, optional
            Controls the visibility of the annotation when it goes
            outside the axes area.

            If `True`, the annotation will only be drawn when the
            ``xy`` is inside the axes. If `False`, the annotation will
            always be drawn regardless of its position.

            The default is `None`, which behave as `True` only if
            *xycoords* is "data".

        Returns
        -------
        Annotation

        '''

        _AnnotationBase.__init__(self,
                                 xy,
                                 xycoords=xycoords,
                                 annotation_clip=annotation_clip)
        # warn about wonky input data
        if (xytext is None and
                textcoords is not None and
                textcoords != xycoords):
            warnings.warn("You have used the `textcoords` kwarg, but not "
                          "the `xytext` kwarg.  This can lead to surprising "
                          "results.")

        # clean up textcoords and assign default
        if textcoords is None:
            textcoords = self.xycoords
        self._textcoords = textcoords

        # cleanup xytext defaults
        if xytext is None:
            xytext = self.xy
        x, y = xytext

        Text.__init__(self, x, y, s, **kwargs)

        self.arrowprops = arrowprops

        self.arrow = None

        if arrowprops is not None:
            if "arrowstyle" in arrowprops:
                arrowprops = self.arrowprops.copy()
                self._arrow_relpos = arrowprops.pop("relpos", (0.5, 0.5))
            else:
                # modified YAArrow API to be used with FancyArrowPatch
                shapekeys = ('width', 'headwidth', 'headlength',
                             'shrink', 'frac')
                arrowprops = dict()
                for key, val in self.arrowprops.items():
                    if key not in shapekeys:
                        arrowprops[key] = val  # basic Patch properties
            self.arrow_patch = FancyArrowPatch((0, 0), (1, 1),
                                               **arrowprops)
        else:
            self.arrow_patch = None
