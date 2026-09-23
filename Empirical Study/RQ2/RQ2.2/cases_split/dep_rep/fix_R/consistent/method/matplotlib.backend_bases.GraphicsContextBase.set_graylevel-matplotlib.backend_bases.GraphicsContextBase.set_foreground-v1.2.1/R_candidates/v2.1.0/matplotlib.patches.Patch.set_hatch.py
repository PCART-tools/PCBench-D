    def set_hatch(self, hatch):
        """
        Set the hatching pattern

        *hatch* can be one of::

          /   - diagonal hatching
          \\   - back diagonal
          |   - vertical
          -   - horizontal
          +   - crossed
          x   - crossed diagonal
          o   - small circle
          O   - large circle
          .   - dots
          *   - stars

        Letters can be combined, in which case all the specified
        hatchings are done.  If same letter repeats, it increases the
        density of hatching of that pattern.

        Hatching is supported in the PostScript, PDF, SVG and Agg
        backends only.

        ACCEPTS: ['/' | '\\\\' | '|' | '-' | '+' | 'x' | 'o' | 'O' | '.' | '*']
        """
        self._hatch = hatch
        self.stale = True
