    @docstring.dedent_interpd
    def __init__(self, xyA, xyB, coordsA, coordsB=None,
                 axesA=None, axesB=None,
                 arrowstyle="-",
                 connectionstyle="arc3",
                 patchA=None,
                 patchB=None,
                 shrinkA=0.,
                 shrinkB=0.,
                 mutation_scale=10.,
                 mutation_aspect=None,
                 clip_on=False,
                 dpi_cor=1.,
                 **kwargs):
        """
        Connect point *xyA* in *coordsA* with point *xyB* in *coordsB*.

        Valid keys are

        ===============  ======================================================
        Key              Description
        ===============  ======================================================
        arrowstyle       the arrow style
        connectionstyle  the connection style
        relpos           default is (0.5, 0.5)
        patchA           default is bounding box of the text
        patchB           default is None
        shrinkA          default is 2 points
        shrinkB          default is 2 points
        mutation_scale   default is text size (in points)
        mutation_aspect  default is 1.
        ?                any key for `matplotlib.patches.PathPatch`
        ===============  ======================================================

        *coordsA* and *coordsB* are strings that indicate the
        coordinates of *xyA* and *xyB*.

        =================  ===================================================
        Property           Description
        =================  ===================================================
        'figure points'    points from the lower left corner of the figure
        'figure pixels'    pixels from the lower left corner of the figure
        'figure fraction'  0, 0 is lower left of figure and 1, 1 is upper right
        'axes points'      points from lower left corner of axes
        'axes pixels'      pixels from lower left corner of axes
        'axes fraction'    0, 0 is lower left of axes and 1, 1 is upper right
        'data'             use the coordinate system of the object being
                           annotated (default)
        'offset points'    offset (in points) from the *xy* value
        'polar'            you can specify *theta*, *r* for the annotation,
                           even in cartesian plots.  Note that if you are using
                           a polar axes, you do not need to specify polar for
                           the coordinate system since that is the native
                           "data" coordinate system.
        =================  ===================================================

        Alternatively they can be set to any valid
        `~matplotlib.transforms.Transform`.

        .. note::

           Using `ConnectionPatch` across two `~.axes.Axes` instances
           is not directly compatible with :doc:`constrained layout
           </tutorials/intermediate/constrainedlayout_guide>`. Add the artist
           directly to the `.Figure` instead of adding it to a specific Axes.

           .. code-block:: default

              fig, ax = plt.subplots(1, 2, constrained_layout=True)
              con = ConnectionPatch(..., axesA=ax[0], axesB=ax[1])
              fig.add_artist(con)

        """
        if coordsB is None:
            coordsB = coordsA
        # we'll draw ourself after the artist we annotate by default
        self.xy1 = xyA
        self.xy2 = xyB
        self.coords1 = coordsA
        self.coords2 = coordsB

        self.axesA = axesA
        self.axesB = axesB

        FancyArrowPatch.__init__(self,
                                 posA=(0, 0), posB=(1, 1),
                                 arrowstyle=arrowstyle,
                                 connectionstyle=connectionstyle,
                                 patchA=patchA,
                                 patchB=patchB,
                                 shrinkA=shrinkA,
                                 shrinkB=shrinkB,
                                 mutation_scale=mutation_scale,
                                 mutation_aspect=mutation_aspect,
                                 clip_on=clip_on,
                                 dpi_cor=dpi_cor,
                                 **kwargs)

        # if True, draw annotation only if self.xy is inside the axes
        self._annotation_clip = None
