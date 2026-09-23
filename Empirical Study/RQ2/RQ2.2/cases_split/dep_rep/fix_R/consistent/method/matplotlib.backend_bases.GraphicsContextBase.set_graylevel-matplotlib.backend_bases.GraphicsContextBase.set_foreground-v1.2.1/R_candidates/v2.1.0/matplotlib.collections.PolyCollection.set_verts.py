    def set_verts(self, verts, closed=True):
        '''This allows one to delay initialization of the vertices.'''
        if isinstance(verts, np.ma.MaskedArray):
            verts = verts.astype(float).filled(np.nan)
            # This is much faster than having Path do it one at a time.
        if closed:
            self._paths = []
            for xy in verts:
                if len(xy):
                    if isinstance(xy, np.ma.MaskedArray):
                        xy = np.ma.concatenate([xy, xy[0:1]])
                    else:
                        xy = np.asarray(xy)
                        xy = np.concatenate([xy, xy[0:1]])
                    codes = np.empty(xy.shape[0], dtype=mpath.Path.code_type)
                    codes[:] = mpath.Path.LINETO
                    codes[0] = mpath.Path.MOVETO
                    codes[-1] = mpath.Path.CLOSEPOLY
                    self._paths.append(mpath.Path(xy, codes))
                else:
                    self._paths.append(mpath.Path(xy))
        else:
            self._paths = [mpath.Path(xy) for xy in verts]
        self.stale = True
