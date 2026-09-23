        def transmute(self, path, mutation_size, linewidth):

            head_length = self.head_length * mutation_size
            head_width = self.head_width * mutation_size
            head_dist = math.sqrt(head_length ** 2 + head_width ** 2)
            cos_t, sin_t = head_length / head_dist, head_width / head_dist

            # begin arrow
            x0, y0 = path.vertices[0]
            x1, y1 = path.vertices[1]

            # If there is no room for an arrow and a line, then skip the arrow
            has_begin_arrow = self.beginarrow and not (x0 == x1 and y0 == y1)
            if has_begin_arrow:
                verticesA, codesA, ddxA, ddyA = \
                           self._get_arrow_wedge(x1, y1, x0, y0,
                                                 head_dist, cos_t, sin_t,
                                                 linewidth)
            else:
                verticesA, codesA = [], []
                ddxA, ddyA = 0., 0.

            # end arrow
            x2, y2 = path.vertices[-2]
            x3, y3 = path.vertices[-1]

            # If there is no room for an arrow and a line, then skip the arrow
            has_end_arrow = (self.endarrow and not ((x2 == x3) and (y2 == y3)))
            if has_end_arrow:
                verticesB, codesB, ddxB, ddyB = \
                           self._get_arrow_wedge(x2, y2, x3, y3,
                                                 head_dist, cos_t, sin_t,
                                                 linewidth)
            else:
                verticesB, codesB = [], []
                ddxB, ddyB = 0., 0.

            # this simple code will not work if ddx, ddy is greater than
            # separation bettern vertices.
            _path = [Path(np.concatenate([[(x0 + ddxA, y0 + ddyA)],
                                          path.vertices[1:-1],
                                          [(x3 + ddxB, y3 + ddyB)]]),
                          path.codes)]
            _fillable = [False]

            if has_begin_arrow:
                if self.fillbegin:
                    p = np.concatenate([verticesA, [verticesA[0],
                                                    verticesA[0]], ])
                    c = np.concatenate([codesA, [Path.LINETO, Path.CLOSEPOLY]])
                    _path.append(Path(p, c))
                    _fillable.append(True)
                else:
                    _path.append(Path(verticesA, codesA))
                    _fillable.append(False)

            if has_end_arrow:
                if self.fillend:
                    _fillable.append(True)
                    p = np.concatenate([verticesB, [verticesB[0],
                                                    verticesB[0]], ])
                    c = np.concatenate([codesB, [Path.LINETO, Path.CLOSEPOLY]])
                    _path.append(Path(p, c))
                else:
                    _fillable.append(False)
                    _path.append(Path(verticesB, codesB))

            return _path, _fillable
