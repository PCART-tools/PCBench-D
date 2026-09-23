    def _determine_order(self, totals):
        """
        A helper function to determine the highest order of glue
        used by the members of this list.  Used by vpack and hpack.
        """
        o = 0
        for i in range(len(totals) - 1, 0, -1):
            if totals[i] != 0.0:
                o = i
                break
        return o
