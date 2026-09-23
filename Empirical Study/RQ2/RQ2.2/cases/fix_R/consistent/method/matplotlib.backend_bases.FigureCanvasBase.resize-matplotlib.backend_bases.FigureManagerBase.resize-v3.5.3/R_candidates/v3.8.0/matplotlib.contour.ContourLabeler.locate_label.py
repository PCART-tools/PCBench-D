    def locate_label(self, linecontour, labelwidth):
        """
        Find good place to draw a label (relatively flat part of the contour).
        """
        ctr_size = len(linecontour)
        n_blocks = int(np.ceil(ctr_size / labelwidth)) if labelwidth > 1 else 1
        block_size = ctr_size if n_blocks == 1 else int(labelwidth)
        # Split contour into blocks of length ``block_size``, filling the last
        # block by cycling the contour start (per `np.resize` semantics).  (Due
        # to cycling, the index returned is taken modulo ctr_size.)
        xx = np.resize(linecontour[:, 0], (n_blocks, block_size))
        yy = np.resize(linecontour[:, 1], (n_blocks, block_size))
        yfirst = yy[:, :1]
        ylast = yy[:, -1:]
        xfirst = xx[:, :1]
        xlast = xx[:, -1:]
        s = (yfirst - yy) * (xlast - xfirst) - (xfirst - xx) * (ylast - yfirst)
        l = np.hypot(xlast - xfirst, ylast - yfirst)
        # Ignore warning that divide by zero throws, as this is a valid option
        with np.errstate(divide='ignore', invalid='ignore'):
            distances = (abs(s) / l).sum(axis=-1)
        # Labels are drawn in the middle of the block (``hbsize``) where the
        # contour is the closest (per ``distances``) to a straight line, but
        # not `too_close()` to a preexisting label.
        hbsize = block_size // 2
        adist = np.argsort(distances)
        # If all candidates are `too_close()`, go back to the straightest part
        # (``adist[0]``).
        for idx in np.append(adist, adist[0]):
            x, y = xx[idx, hbsize], yy[idx, hbsize]
            if not self.too_close(x, y, labelwidth):
                break
        return x, y, (idx * block_size + hbsize) % ctr_size
