    def draw_path(self, gc, path, transform, rgbFace=None):
        # docstring inherited
        nmax = mpl.rcParams['agg.path.chunksize']  # here at least for testing
        npts = path.vertices.shape[0]

        if (npts > nmax > 100 and path.should_simplify and
                rgbFace is None and gc.get_hatch() is None):
            nch = np.ceil(npts / nmax)
            chsize = int(np.ceil(npts / nch))
            i0 = np.arange(0, npts, chsize)
            i1 = np.zeros_like(i0)
            i1[:-1] = i0[1:] - 1
            i1[-1] = npts
            for ii0, ii1 in zip(i0, i1):
                v = path.vertices[ii0:ii1, :]
                c = path.codes
                if c is not None:
                    c = c[ii0:ii1]
                    c[0] = Path.MOVETO  # move to end of last chunk
                p = Path(v, c)
                try:
                    self._renderer.draw_path(gc, p, transform, rgbFace)
                except OverflowError as err:
                    raise OverflowError(
                        "Exceeded cell block limit (set 'agg.path.chunksize' "
                        "rcparam)") from err
        else:
            try:
                self._renderer.draw_path(gc, path, transform, rgbFace)
            except OverflowError as err:
                raise OverflowError("Exceeded cell block limit (set "
                                    "'agg.path.chunksize' rcparam)") from err
