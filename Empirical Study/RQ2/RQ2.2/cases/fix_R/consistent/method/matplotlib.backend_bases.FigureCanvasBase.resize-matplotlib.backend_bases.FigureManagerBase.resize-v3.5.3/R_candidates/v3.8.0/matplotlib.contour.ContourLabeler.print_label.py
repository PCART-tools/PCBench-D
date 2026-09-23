    def print_label(self, linecontour, labelwidth):
        """Return whether a contour is long enough to hold a label."""
        return (len(linecontour) > 10 * labelwidth
                or (len(linecontour)
                    and (np.ptp(linecontour, axis=0) > 1.2 * labelwidth).any()))
