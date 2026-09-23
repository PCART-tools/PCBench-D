    @allow_rasterization
    def draw(self, renderer):
        """draw the Line with `renderer` unless visibility is False"""
        if not self.get_visible():
            return

        if self._invalidy or self._invalidx:
            self.recache()
        self.ind_offset = 0  # Needed for contains() method.
        if self._subslice and self.axes:
            x0, x1 = self.axes.get_xbound()
            i0, = self._x_filled.searchsorted([x0], 'left')
            i1, = self._x_filled.searchsorted([x1], 'right')
            subslice = slice(max(i0 - 1, 0), i1 + 1)
            self.ind_offset = subslice.start
            self._transform_path(subslice)

        transf_path = self._get_transformed_path()

        if self.get_path_effects():
            from matplotlib.patheffects import PathEffectRenderer
            renderer = PathEffectRenderer(self.get_path_effects(), renderer)

        renderer.open_group('line2d', self.get_gid())
        if self._lineStyles[self._linestyle] != '_draw_nothing':
            tpath, affine = transf_path.get_transformed_path_and_affine()
            if len(tpath.vertices):
                gc = renderer.new_gc()
                self._set_gc_clip(gc)

                ln_color_rgba = self._get_rgba_ln_color()
                gc.set_foreground(ln_color_rgba, isRGBA=True)
                gc.set_alpha(ln_color_rgba[3])

                gc.set_antialiased(self._antialiased)
                gc.set_linewidth(self._linewidth)

                if self.is_dashed():
                    cap = self._dashcapstyle
                    join = self._dashjoinstyle
                else:
                    cap = self._solidcapstyle
                    join = self._solidjoinstyle
                gc.set_joinstyle(join)
                gc.set_capstyle(cap)
                gc.set_snap(self.get_snap())
                if self.get_sketch_params() is not None:
                    gc.set_sketch_params(*self.get_sketch_params())

                gc.set_dashes(self._dashOffset, self._dashSeq)
                renderer.draw_path(gc, tpath, affine.frozen())
                gc.restore()

        if self._marker and self._markersize > 0:
            gc = renderer.new_gc()
            self._set_gc_clip(gc)
            rgbaFace = self._get_rgba_face()
            rgbaFaceAlt = self._get_rgba_face(alt=True)
            edgecolor = self.get_markeredgecolor()
            if (isinstance(edgecolor, six.string_types)
                    and edgecolor.lower() == 'none'):
                gc.set_linewidth(0)
                gc.set_foreground(rgbaFace, isRGBA=True)
            else:
                gc.set_foreground(edgecolor)
                gc.set_linewidth(self._markeredgewidth)
                mec = self._markeredgecolor
                if (isinstance(mec, six.string_types) and mec == 'auto' and
                        rgbaFace is not None):
                    gc.set_alpha(rgbaFace[3])
                else:
                    gc.set_alpha(self.get_alpha())

            marker = self._marker
            tpath, affine = transf_path.get_transformed_points_and_affine()
            if len(tpath.vertices):
                # subsample the markers if markevery is not None
                markevery = self.get_markevery()
                if markevery is not None:
                    subsampled = _mark_every_path(markevery, tpath,
                                                  affine, self.axes.transAxes)
                else:
                    subsampled = tpath

                snap = marker.get_snap_threshold()
                if type(snap) == float:
                    snap = renderer.points_to_pixels(self._markersize) >= snap
                gc.set_snap(snap)
                gc.set_joinstyle(marker.get_joinstyle())
                gc.set_capstyle(marker.get_capstyle())
                marker_path = marker.get_path()
                marker_trans = marker.get_transform()
                w = renderer.points_to_pixels(self._markersize)

                if (isinstance(marker.get_marker(), six.string_types) and
                        marker.get_marker() == ','):
                    gc.set_linewidth(0)
                else:
                    # Don't scale for pixels, and don't stroke them
                    marker_trans = marker_trans.scale(w)

                renderer.draw_markers(gc, marker_path, marker_trans,
                                      subsampled, affine.frozen(),
                                      rgbaFace)

                alt_marker_path = marker.get_alt_path()
                if alt_marker_path:
                    alt_marker_trans = marker.get_alt_transform()
                    alt_marker_trans = alt_marker_trans.scale(w)
                    if (isinstance(mec, six.string_types) and mec == 'auto' and
                            rgbaFaceAlt is not None):
                        gc.set_alpha(rgbaFaceAlt[3])
                    else:
                        gc.set_alpha(self.get_alpha())

                    renderer.draw_markers(
                            gc, alt_marker_path, alt_marker_trans, subsampled,
                            affine.frozen(), rgbaFaceAlt)

            gc.restore()

        renderer.close_group('line2d')
        self.stale = False
