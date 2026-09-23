    class _Bracket(_Base):

        def __init__(self, bracketA=None, bracketB=None,
                     widthA=1., widthB=1.,
                     lengthA=0.2, lengthB=0.2,
                     angleA=None, angleB=None,
                     scaleA=None, scaleB=None):
            self.bracketA, self.bracketB = bracketA, bracketB
            self.widthA, self.widthB = widthA, widthB
            self.lengthA, self.lengthB = lengthA, lengthB
            self.angleA, self.angleB = angleA, angleB
            self.scaleA, self.scaleB = scaleA, scaleB

        def _get_bracket(self, x0, y0,
                         cos_t, sin_t, width, length, angle):

            # arrow from x0, y0 to x1, y1
            from matplotlib.bezier import get_normal_points
            x1, y1, x2, y2 = get_normal_points(x0, y0, cos_t, sin_t, width)

            dx, dy = length * cos_t, length * sin_t

            vertices_arrow = [(x1 + dx, y1 + dy),
                              (x1, y1),
                              (x2, y2),
                              (x2 + dx, y2 + dy)]
            codes_arrow = [Path.MOVETO,
                           Path.LINETO,
                           Path.LINETO,
                           Path.LINETO]

            if angle is not None:
                trans = transforms.Affine2D().rotate_deg_around(x0, y0, angle)
                vertices_arrow = trans.transform(vertices_arrow)

            return vertices_arrow, codes_arrow

        def transmute(self, path, mutation_size, linewidth):

            if self.scaleA is None:
                scaleA = mutation_size
            else:
                scaleA = self.scaleA

            if self.scaleB is None:
                scaleB = mutation_size
            else:
                scaleB = self.scaleB

            vertices_list, codes_list = [], []

            if self.bracketA:
                x0, y0 = path.vertices[0]
                x1, y1 = path.vertices[1]
                cos_t, sin_t = get_cos_sin(x1, y1, x0, y0)
                verticesA, codesA = self._get_bracket(x0, y0, cos_t, sin_t,
                                                      self.widthA * scaleA,
                                                      self.lengthA * scaleA,
                                                      self.angleA)
                vertices_list.append(verticesA)
                codes_list.append(codesA)

            vertices_list.append(path.vertices)
            codes_list.append(path.codes)

            if self.bracketB:
                x0, y0 = path.vertices[-1]
                x1, y1 = path.vertices[-2]
                cos_t, sin_t = get_cos_sin(x1, y1, x0, y0)
                verticesB, codesB = self._get_bracket(x0, y0, cos_t, sin_t,
                                                      self.widthB * scaleB,
                                                      self.lengthB * scaleB,
                                                      self.angleB)
                vertices_list.append(verticesB)
                codes_list.append(codesB)

            vertices = np.concatenate(vertices_list)
            codes = np.concatenate(codes_list)

            p = Path(vertices, codes)

            return p, False
