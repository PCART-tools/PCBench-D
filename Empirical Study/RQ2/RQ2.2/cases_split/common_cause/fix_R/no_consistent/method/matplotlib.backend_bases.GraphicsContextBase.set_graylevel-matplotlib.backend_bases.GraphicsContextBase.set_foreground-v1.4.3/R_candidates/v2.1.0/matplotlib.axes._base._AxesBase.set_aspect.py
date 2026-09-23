    def set_aspect(self, aspect, adjustable=None, anchor=None):
        """
        *aspect*

          ========   ================================================
          value      description
          ========   ================================================
          'auto'     automatic; fill position rectangle with data
          'equal'    same scaling from data to plot units for x and y
           num       a circle will be stretched such that the height
                     is num times the width. aspect=1 is the same as
                     aspect='equal'.
          ========   ================================================

        *adjustable*

          ============   =====================================
          value          description
          ============   =====================================
          'box'          change physical size of axes
          'datalim'      change xlim or ylim
          'box-forced'   same as 'box', but axes can be shared
          ============   =====================================

        'box' does not allow axes sharing, as this can cause
        unintended side effect. For cases when sharing axes is
        fine, use 'box-forced'.

        *anchor*

          =====   =====================
          value   description
          =====   =====================
          'C'     centered
          'SW'    lower left corner
          'S'     middle of bottom edge
          'SE'    lower right corner
          etc.
          =====   =====================
        """
        if (isinstance(aspect, six.string_types)
                and aspect in ('equal', 'auto')):
            self._aspect = aspect
        else:
            self._aspect = float(aspect)  # raise ValueError if necessary

        if adjustable is not None:
            self.set_adjustable(adjustable)
        if anchor is not None:
            self.set_anchor(anchor)
        self.stale = True
