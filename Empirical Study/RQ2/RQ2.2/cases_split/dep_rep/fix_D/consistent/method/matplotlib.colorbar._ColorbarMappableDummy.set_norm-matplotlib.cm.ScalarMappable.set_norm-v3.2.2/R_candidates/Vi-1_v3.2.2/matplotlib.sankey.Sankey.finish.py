    def finish(self):
        """
        Adjust the axes and return a list of information about the Sankey
        subdiagram(s).

        Return value is a list of subdiagrams represented with the following
        fields:

          ===============   ===================================================
          Field             Description
          ===============   ===================================================
          *patch*           Sankey outline (an instance of
                            :class:`~matplotlib.patches.PathPatch`)
          *flows*           values of the flows (positive for input, negative
                            for output)
          *angles*          list of angles of the arrows [deg/90]
                            For example, if the diagram has not been rotated,
                            an input to the top side will have an angle of 3
                            (DOWN), and an output from the top side will have
                            an angle of 1 (UP).  If a flow has been skipped
                            (because its magnitude is less than *tolerance*),
                            then its angle will be *None*.
          *tips*            array in which each row is an [x, y] pair
                            indicating the positions of the tips (or "dips") of
                            the flow paths
                            If the magnitude of a flow is less the *tolerance*
                            for the instance of :class:`Sankey`, the flow is
                            skipped and its tip will be at the center of the
                            diagram.
          *text*            :class:`~matplotlib.text.Text` instance for the
                            label of the diagram
          *texts*           list of :class:`~matplotlib.text.Text` instances
                            for the labels of flows
          ===============   ===================================================

        See Also
        --------
        Sankey.add
        """
        self.ax.axis([self.extent[0] - self.margin,
                      self.extent[1] + self.margin,
                      self.extent[2] - self.margin,
                      self.extent[3] + self.margin])
        self.ax.set_aspect('equal', adjustable='datalim')
        return self.diagrams
