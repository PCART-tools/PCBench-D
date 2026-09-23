class BoxStyle(_Style):
    """
    `BoxStyle` is a container class which defines several
    boxstyle classes, which are used for `FancyBboxPatch`.

    A style object can be created as::

           BoxStyle.Round(pad=0.2)

    or::

           BoxStyle("Round", pad=0.2)

    or::

           BoxStyle("Round, pad=0.2")

    The following boxstyle classes are defined.

    %(AvailableBoxstyles)s

    An instance of any boxstyle class is an callable object,
    whose call signature is::

       __call__(self, x0, y0, width, height, mutation_size)

    and returns a `.Path` instance. *x0*, *y0*, *width* and
    *height* specify the location and size of the box to be
    drawn. *mutation_scale* determines the overall size of the
    mutation (by which I mean the transformation of the rectangle to
    the fancy box).
    """

    _style_list = {}

    @_api.deprecated("3.4")
    class _Base:
        """
        Abstract base class for styling of `.FancyBboxPatch`.

        This class is not an artist itself.  The `__call__` method returns the
        `~matplotlib.path.Path` for outlining the fancy box. The actual drawing
        is handled in `.FancyBboxPatch`.

        Subclasses may only use parameters with default values in their
        ``__init__`` method because they must be able to be initialized
        without arguments.

        Subclasses must implement the `__call__` method. It receives the
        enclosing rectangle *x0, y0, width, height* as well as the
        *mutation_size*, which scales the outline properties such as padding.
        It returns the outline of the fancy box as `.path.Path`.
        """

        @_api.deprecated("3.4")
        def transmute(self, x0, y0, width, height, mutation_size):
            """Return the `~.path.Path` outlining the given rectangle."""
            return self(self, x0, y0, width, height, mutation_size, 1)

        # This can go away once the deprecation period elapses, leaving _Base
        # as a fully abstract base class just providing docstrings, no logic.
        def __init_subclass__(cls):
            transmute = _api.deprecate_method_override(
                __class__.transmute, cls, since="3.4")
            if transmute:
                cls.__call__ = transmute
                return

            __call__ = cls.__call__

            @_api.delete_parameter("3.4", "mutation_aspect")
            def call_wrapper(
                    self, x0, y0, width, height, mutation_size,
                    mutation_aspect=_api.deprecation._deprecated_parameter):
                if mutation_aspect is _api.deprecation._deprecated_parameter:
                    # Don't trigger deprecation warning internally.
                    return __call__(self, x0, y0, width, height, mutation_size)
                else:
                    # Squeeze the given height by the aspect_ratio.
                    y0, height = y0 / mutation_aspect, height / mutation_aspect
                    path = self(x0, y0, width, height, mutation_size,
                                mutation_aspect)
                    vertices, codes = path.vertices, path.codes
                    # Restore the height.
                    vertices[:, 1] = vertices[:, 1] * mutation_aspect
                    return Path(vertices, codes)

            cls.__call__ = call_wrapper

        def __call__(self, x0, y0, width, height, mutation_size):
            """
            Given the location and size of the box, return the path of
            the box around it.

            Parameters
            ----------
            x0, y0, width, height : float
                Location and size of the box.
            mutation_size : float
                A reference scale for the mutation.

            Returns
            -------
            `~matplotlib.path.Path`
            """
            raise NotImplementedError('Derived must override')

    @_register_style(_style_list)
    class Square(_Base):
        """A square box."""

        def __init__(self, pad=0.3):
            """
            Parameters
            ----------
            pad : float, default: 0.3
                The amount of padding around the original box.
            """
            self.pad = pad

        def __call__(self, x0, y0, width, height, mutation_size):
            pad = mutation_size * self.pad
            # width and height with padding added.
            width, height = width + 2 * pad, height + 2 * pad
            # boundary of the padded box
            x0, y0 = x0 - pad, y0 - pad
            x1, y1 = x0 + width, y0 + height
            return Path([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)],
                        closed=True)

    @_register_style(_style_list)
    class Circle(_Base):
        """A circular box."""

        def __init__(self, pad=0.3):
            """
            Parameters
            ----------
            pad : float, default: 0.3
                The amount of padding around the original box.
            """
            self.pad = pad

        def __call__(self, x0, y0, width, height, mutation_size):
            pad = mutation_size * self.pad
            width, height = width + 2 * pad, height + 2 * pad
            # boundary of the padded box
            x0, y0 = x0 - pad, y0 - pad
            return Path.circle((x0 + width / 2, y0 + height / 2),
                               max(width, height) / 2)

    @_register_style(_style_list)
    class LArrow(_Base):
        """A box in the shape of a left-pointing arrow."""

        def __init__(self, pad=0.3):
            """
            Parameters
            ----------
            pad : float, default: 0.3
                The amount of padding around the original box.
            """
            self.pad = pad

        def __call__(self, x0, y0, width, height, mutation_size):
            # padding
            pad = mutation_size * self.pad
            # width and height with padding added.
            width, height = width + 2 * pad, height + 2 * pad
            # boundary of the padded box
            x0, y0 = x0 - pad, y0 - pad,
            x1, y1 = x0 + width, y0 + height

            dx = (y1 - y0) / 2
            dxx = dx / 2
            x0 = x0 + pad / 1.4  # adjust by ~sqrt(2)

            return Path([(x0 + dxx, y0), (x1, y0), (x1, y1), (x0 + dxx, y1),
                         (x0 + dxx, y1 + dxx), (x0 - dx, y0 + dx),
                         (x0 + dxx, y0 - dxx),  # arrow
                         (x0 + dxx, y0), (x0 + dxx, y0)],
                        closed=True)

    @_register_style(_style_list)
    class RArrow(LArrow):
        """A box in the shape of a right-pointing arrow."""

        def __call__(self, x0, y0, width, height, mutation_size):
            p = BoxStyle.LArrow.__call__(
                self, x0, y0, width, height, mutation_size)
            p.vertices[:, 0] = 2 * x0 + width - p.vertices[:, 0]
            return p

    @_register_style(_style_list)
    class DArrow(_Base):
        """A box in the shape of a two-way arrow."""
        # Modified from LArrow to add a right arrow to the bbox.

        def __init__(self, pad=0.3):
            """
            Parameters
            ----------
            pad : float, default: 0.3
                The amount of padding around the original box.
            """
            self.pad = pad

        def __call__(self, x0, y0, width, height, mutation_size):
            # padding
            pad = mutation_size * self.pad
            # width and height with padding added.
            # The width is padded by the arrows, so we don't need to pad it.
            height = height + 2 * pad
            # boundary of the padded box
            x0, y0 = x0 - pad, y0 - pad
            x1, y1 = x0 + width, y0 + height

            dx = (y1 - y0) / 2
            dxx = dx / 2
            x0 = x0 + pad / 1.4  # adjust by ~sqrt(2)

            return Path([(x0 + dxx, y0), (x1, y0),  # bot-segment
                         (x1, y0 - dxx), (x1 + dx + dxx, y0 + dx),
                         (x1, y1 + dxx),  # right-arrow
                         (x1, y1), (x0 + dxx, y1),  # top-segment
                         (x0 + dxx, y1 + dxx), (x0 - dx, y0 + dx),
                         (x0 + dxx, y0 - dxx),  # left-arrow
                         (x0 + dxx, y0), (x0 + dxx, y0)],  # close-poly
                        closed=True)

    @_register_style(_style_list)
    class Round(_Base):
        """A box with round corners."""

        def __init__(self, pad=0.3, rounding_size=None):
            """
            Parameters
            ----------
            pad : float, default: 0.3
                The amount of padding around the original box.
            rounding_size : float, default: *pad*
                Radius of the corners.
            """
            self.pad = pad
            self.rounding_size = rounding_size

        def __call__(self, x0, y0, width, height, mutation_size):

            # padding
            pad = mutation_size * self.pad

            # size of the rounding corner
            if self.rounding_size:
                dr = mutation_size * self.rounding_size
            else:
                dr = pad

            width, height = width + 2 * pad, height + 2 * pad

            x0, y0 = x0 - pad, y0 - pad,
            x1, y1 = x0 + width, y0 + height

            # Round corners are implemented as quadratic Bezier, e.g.,
            # [(x0, y0-dr), (x0, y0), (x0+dr, y0)] for lower left corner.
            cp = [(x0 + dr, y0),
                  (x1 - dr, y0),
                  (x1, y0), (x1, y0 + dr),
                  (x1, y1 - dr),
                  (x1, y1), (x1 - dr, y1),
                  (x0 + dr, y1),
                  (x0, y1), (x0, y1 - dr),
                  (x0, y0 + dr),
                  (x0, y0), (x0 + dr, y0),
                  (x0 + dr, y0)]

            com = [Path.MOVETO,
                   Path.LINETO,
                   Path.CURVE3, Path.CURVE3,
                   Path.LINETO,
                   Path.CURVE3, Path.CURVE3,
                   Path.LINETO,
                   Path.CURVE3, Path.CURVE3,
                   Path.LINETO,
                   Path.CURVE3, Path.CURVE3,
                   Path.CLOSEPOLY]

            path = Path(cp, com)

            return path

    @_register_style(_style_list)
    class Round4(_Base):
        """A box with rounded edges."""

        def __init__(self, pad=0.3, rounding_size=None):
            """
            Parameters
            ----------
            pad : float, default: 0.3
                The amount of padding around the original box.
            rounding_size : float, default: *pad*/2
                Rounding of edges.
            """
            self.pad = pad
            self.rounding_size = rounding_size

        def __call__(self, x0, y0, width, height, mutation_size):

            # padding
            pad = mutation_size * self.pad

            # Rounding size; defaults to half of the padding.
            if self.rounding_size:
                dr = mutation_size * self.rounding_size
            else:
                dr = pad / 2.

            width = width + 2 * pad - 2 * dr
            height = height + 2 * pad - 2 * dr

            x0, y0 = x0 - pad + dr, y0 - pad + dr,
            x1, y1 = x0 + width, y0 + height

            cp = [(x0, y0),
                  (x0 + dr, y0 - dr), (x1 - dr, y0 - dr), (x1, y0),
                  (x1 + dr, y0 + dr), (x1 + dr, y1 - dr), (x1, y1),
                  (x1 - dr, y1 + dr), (x0 + dr, y1 + dr), (x0, y1),
                  (x0 - dr, y1 - dr), (x0 - dr, y0 + dr), (x0, y0),
                  (x0, y0)]

            com = [Path.MOVETO,
                   Path.CURVE4, Path.CURVE4, Path.CURVE4,
                   Path.CURVE4, Path.CURVE4, Path.CURVE4,
                   Path.CURVE4, Path.CURVE4, Path.CURVE4,
                   Path.CURVE4, Path.CURVE4, Path.CURVE4,
                   Path.CLOSEPOLY]

            path = Path(cp, com)

            return path

    @_register_style(_style_list)
    class Sawtooth(_Base):
        """A box with a sawtooth outline."""

        def __init__(self, pad=0.3, tooth_size=None):
            """
            Parameters
            ----------
            pad : float, default: 0.3
                The amount of padding around the original box.
            tooth_size : float, default: *pad*/2
                Size of the sawtooth.
            """
            self.pad = pad
            self.tooth_size = tooth_size

        def _get_sawtooth_vertices(self, x0, y0, width, height, mutation_size):

            # padding
            pad = mutation_size * self.pad

            # size of sawtooth
            if self.tooth_size is None:
                tooth_size = self.pad * .5 * mutation_size
            else:
                tooth_size = self.tooth_size * mutation_size

            tooth_size2 = tooth_size / 2
            width = width + 2 * pad - tooth_size
            height = height + 2 * pad - tooth_size

            # the sizes of the vertical and horizontal sawtooth are
            # separately adjusted to fit the given box size.
            dsx_n = int(round((width - tooth_size) / (tooth_size * 2))) * 2
            dsx = (width - tooth_size) / dsx_n
            dsy_n = int(round((height - tooth_size) / (tooth_size * 2))) * 2
            dsy = (height - tooth_size) / dsy_n

            x0, y0 = x0 - pad + tooth_size2, y0 - pad + tooth_size2
            x1, y1 = x0 + width, y0 + height

            bottom_saw_x = [
                x0,
                *(x0 + tooth_size2 + dsx * .5 * np.arange(dsx_n * 2)),
                x1 - tooth_size2,
            ]
            bottom_saw_y = [
                y0,
                *([y0 - tooth_size2, y0, y0 + tooth_size2, y0] * dsx_n),
                y0 - tooth_size2,
            ]
            right_saw_x = [
                x1,
                *([x1 + tooth_size2, x1, x1 - tooth_size2, x1] * dsx_n),
                x1 + tooth_size2,
            ]
            right_saw_y = [
                y0,
                *(y0 + tooth_size2 + dsy * .5 * np.arange(dsy_n * 2)),
                y1 - tooth_size2,
            ]
            top_saw_x = [
                x1,
                *(x1 - tooth_size2 - dsx * .5 * np.arange(dsx_n * 2)),
                x0 + tooth_size2,
            ]
            top_saw_y = [
                y1,
                *([y1 + tooth_size2, y1, y1 - tooth_size2, y1] * dsx_n),
                y1 + tooth_size2,
            ]
            left_saw_x = [
                x0,
                *([x0 - tooth_size2, x0, x0 + tooth_size2, x0] * dsy_n),
                x0 - tooth_size2,
            ]
            left_saw_y = [
                y1,
                *(y1 - tooth_size2 - dsy * .5 * np.arange(dsy_n * 2)),
                y0 + tooth_size2,
            ]

            saw_vertices = [*zip(bottom_saw_x, bottom_saw_y),
                            *zip(right_saw_x, right_saw_y),
                            *zip(top_saw_x, top_saw_y),
                            *zip(left_saw_x, left_saw_y),
                            (bottom_saw_x[0], bottom_saw_y[0])]

            return saw_vertices

        def __call__(self, x0, y0, width, height, mutation_size):
            saw_vertices = self._get_sawtooth_vertices(x0, y0, width,
                                                       height, mutation_size)
            path = Path(saw_vertices, closed=True)
            return path

    @_register_style(_style_list)
    class Roundtooth(Sawtooth):
        """A box with a rounded sawtooth outline."""

        def __call__(self, x0, y0, width, height, mutation_size):
            saw_vertices = self._get_sawtooth_vertices(x0, y0,
                                                       width, height,
                                                       mutation_size)
            # Add a trailing vertex to allow us to close the polygon correctly
            saw_vertices = np.concatenate([saw_vertices, [saw_vertices[0]]])
            codes = ([Path.MOVETO] +
                     [Path.CURVE3, Path.CURVE3] * ((len(saw_vertices)-1)//2) +
                     [Path.CLOSEPOLY])
            return Path(saw_vertices, codes)
