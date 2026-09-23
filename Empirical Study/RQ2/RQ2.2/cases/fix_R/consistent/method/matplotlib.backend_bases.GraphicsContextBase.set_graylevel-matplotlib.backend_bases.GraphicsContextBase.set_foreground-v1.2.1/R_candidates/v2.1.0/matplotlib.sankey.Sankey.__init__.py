    def __init__(self, ax=None, scale=1.0, unit='', format='%G', gap=0.25,
                 radius=0.1, shoulder=0.03, offset=0.15, head_angle=100,
                 margin=0.4, tolerance=1e-6, **kwargs):
        """
        Create a new Sankey instance.

        Optional keyword arguments:

          ===============   ===================================================
          Field             Description
          ===============   ===================================================
          *ax*              axes onto which the data should be plotted
                            If *ax* isn't provided, new axes will be created.
          *scale*           scaling factor for the flows
                            *scale* sizes the width of the paths in order to
                            maintain proper layout.  The same scale is applied
                            to all subdiagrams.  The value should be chosen
                            such that the product of the scale and the sum of
                            the inputs is approximately 1.0 (and the product of
                            the scale and the sum of the outputs is
                            approximately -1.0).
          *unit*            string representing the physical unit associated
                            with the flow quantities
                            If *unit* is None, then none of the quantities are
                            labeled.
          *format*          a Python number formatting string to be used in
                            labeling the flow as a quantity (i.e., a number
                            times a unit, where the unit is given)
          *gap*             space between paths that break in/break away
                            to/from the top or bottom
          *radius*          inner radius of the vertical paths
          *shoulder*        size of the shoulders of output arrowS
          *offset*          text offset (from the dip or tip of the arrow)
          *head_angle*      angle of the arrow heads (and negative of the angle
                            of the tails) [deg]
          *margin*          minimum space between Sankey outlines and the edge
                            of the plot area
          *tolerance*       acceptable maximum of the magnitude of the sum of
                            flows
                            The magnitude of the sum of connected flows cannot
                            be greater than *tolerance*.
          ===============   ===================================================

        The optional arguments listed above are applied to all subdiagrams so
        that there is consistent alignment and formatting.

        If :class:`Sankey` is instantiated with any keyword arguments other
        than those explicitly listed above (``**kwargs``), they will be passed
        to :meth:`add`, which will create the first subdiagram.

        In order to draw a complex Sankey diagram, create an instance of
        :class:`Sankey` by calling it without any kwargs::

            sankey = Sankey()

        Then add simple Sankey sub-diagrams::

            sankey.add() # 1
            sankey.add() # 2
            #...
            sankey.add() # n

        Finally, create the full diagram::

            sankey.finish()

        Or, instead, simply daisy-chain those calls::

            Sankey().add().add...  .add().finish()

        .. seealso::

            :meth:`add`
            :meth:`finish`


        **Examples:**

            .. plot:: gallery/api/sankey_basics.py
        """
        # Check the arguments.
        if gap < 0:
            raise ValueError(
            "The gap is negative.\nThis isn't allowed because it "
            "would cause the paths to overlap.")
        if radius > gap:
            raise ValueError(
            "The inner radius is greater than the path spacing.\n"
            "This isn't allowed because it would cause the paths to overlap.")
        if head_angle < 0:
            raise ValueError(
            "The angle is negative.\nThis isn't allowed "
            "because it would cause inputs to look like "
            "outputs and vice versa.")
        if tolerance < 0:
            raise ValueError(
            "The tolerance is negative.\nIt must be a magnitude.")

        # Create axes if necessary.
        if ax is None:
            import matplotlib.pyplot as plt
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[])

        self.diagrams = []

        # Store the inputs.
        self.ax = ax
        self.unit = unit
        self.format = format
        self.scale = scale
        self.gap = gap
        self.radius = radius
        self.shoulder = shoulder
        self.offset = offset
        self.margin = margin
        self.pitch = np.tan(np.pi * (1 - head_angle / 180.0) / 2.0)
        self.tolerance = tolerance

        # Initialize the vertices of tight box around the diagram(s).
        self.extent = np.array((np.inf, -np.inf, np.inf, -np.inf))

        # If there are any kwargs, create the first subdiagram.
        if len(kwargs):
            self.add(**kwargs)
