    def print_label(self, linecontour, labelwidth):
        "Return *False* if contours are too short for a label."
        return (len(linecontour) > 10 * labelwidth
                or (np.ptp(linecontour, axis=0) > 1.2 * labelwidth).any())
