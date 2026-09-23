    def too_close(self, x, y, lw):
        "Return *True* if a label is already near this location."
        for loc in self.labelXYs:
            d = np.sqrt((x - loc[0]) ** 2 + (y - loc[1]) ** 2)
            if d < 1.2 * lw:
                return True
        return False
