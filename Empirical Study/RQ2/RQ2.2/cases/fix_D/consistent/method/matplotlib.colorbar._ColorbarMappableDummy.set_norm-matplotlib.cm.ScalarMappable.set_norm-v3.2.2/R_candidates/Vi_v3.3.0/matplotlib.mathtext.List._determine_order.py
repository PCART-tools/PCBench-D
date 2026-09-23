    @staticmethod
    def _determine_order(totals):
        """
        Determine the highest order of glue used by the members of this list.

        Helper function used by vpack and hpack.
        """
        for i in range(len(totals))[::-1]:
            if totals[i] != 0:
                return i
        return 0
