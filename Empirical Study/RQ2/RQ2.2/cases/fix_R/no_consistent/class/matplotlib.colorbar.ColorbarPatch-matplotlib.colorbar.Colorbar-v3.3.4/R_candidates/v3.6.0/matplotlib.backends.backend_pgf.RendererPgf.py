class RendererPgf(RendererBase):

    def __init__(self, figure, fh):
        """
        Create a new PGF renderer that translates any drawing instruction
        into text commands to be interpreted in a latex pgfpicture environment.

        Attributes
        ----------
        figure : `matplotlib.figure.Figure`
            Matplotlib figure to initialize height, width and dpi from.
        fh : file-like
            File handle for the output of the drawing commands.
        """

        super().__init__()
        self.dpi = figure.dpi
        self.fh = fh
        self.figure = figure
        self.image_counter = 0

    def draw_markers(self, gc, marker_path, marker_trans, path, trans,
                     rgbFace=None):
        # docstring inherited

        _writeln(self.fh, r"\begin{pgfscope}")

        # convert from display units to in
        f = 1. / self.dpi

        # set style and clip
        self._print_pgf_clip(gc)
        self._print_pgf_path_styles(gc, rgbFace)

        # build marker definition
        bl, tr = marker_path.get_extents(marker_trans).get_points()
        coords = bl[0] * f, bl[1] * f, tr[0] * f, tr[1] * f
        _writeln(self.fh,
                 r"\pgfsys@defobject{currentmarker}"
                 r"{\pgfqpoint{%fin}{%fin}}{\pgfqpoint{%fin}{%fin}}{" % coords)
        self._print_pgf_path(None, marker_path, marker_trans)
        self._pgf_path_draw(stroke=gc.get_linewidth() != 0.0,
                            fill=rgbFace is not None)
        _writeln(self.fh, r"}")

        maxcoord = 16383 / 72.27 * self.dpi  # Max dimensions in LaTeX.
        clip = (-maxcoord, -maxcoord, maxcoord, maxcoord)

        # draw marker for each vertex
        for point, code in path.iter_segments(trans, simplify=False,
                                              clip=clip):
            x, y = point[0] * f, point[1] * f
            _writeln(self.fh, r"\begin{pgfscope}")
            _writeln(self.fh, r"\pgfsys@transformshift{%fin}{%fin}" % (x, y))
            _writeln(self.fh, r"\pgfsys@useobject{currentmarker}{}")
            _writeln(self.fh, r"\end{pgfscope}")

        _writeln(self.fh, r"\end{pgfscope}")

    def draw_path(self, gc, path, transform, rgbFace=None):
        # docstring inherited
        _writeln(self.fh, r"\begin{pgfscope}")
        # draw the path
        self._print_pgf_clip(gc)
        self._print_pgf_path_styles(gc, rgbFace)
        self._print_pgf_path(gc, path, transform, rgbFace)
        self._pgf_path_draw(stroke=gc.get_linewidth() != 0.0,
                            fill=rgbFace is not None)
        _writeln(self.fh, r"\end{pgfscope}")

        # if present, draw pattern on top
        if gc.get_hatch():
            _writeln(self.fh, r"\begin{pgfscope}")
            self._print_pgf_path_styles(gc, rgbFace)

            # combine clip and path for clipping
            self._print_pgf_clip(gc)
            self._print_pgf_path(gc, path, transform, rgbFace)
            _writeln(self.fh, r"\pgfusepath{clip}")

            # build pattern definition
            _writeln(self.fh,
                     r"\pgfsys@defobject{currentpattern}"
                     r"{\pgfqpoint{0in}{0in}}{\pgfqpoint{1in}{1in}}{")
            _writeln(self.fh, r"\begin{pgfscope}")
            _writeln(self.fh,
                     r"\pgfpathrectangle"
                     r"{\pgfqpoint{0in}{0in}}{\pgfqpoint{1in}{1in}}")
            _writeln(self.fh, r"\pgfusepath{clip}")
            scale = mpl.transforms.Affine2D().scale(self.dpi)
            self._print_pgf_path(None, gc.get_hatch_path(), scale)
            self._pgf_path_draw(stroke=True)
            _writeln(self.fh, r"\end{pgfscope}")
            _writeln(self.fh, r"}")
            # repeat pattern, filling the bounding rect of the path
            f = 1. / self.dpi
            (xmin, ymin), (xmax, ymax) = \
                path.get_extents(transform).get_points()
            xmin, xmax = f * xmin, f * xmax
            ymin, ymax = f * ymin, f * ymax
            repx, repy = math.ceil(xmax - xmin), math.ceil(ymax - ymin)
            _writeln(self.fh,
                     r"\pgfsys@transformshift{%fin}{%fin}" % (xmin, ymin))
            for iy in range(repy):
                for ix in range(repx):
                    _writeln(self.fh, r"\pgfsys@useobject{currentpattern}{}")
                    _writeln(self.fh, r"\pgfsys@transformshift{1in}{0in}")
                _writeln(self.fh, r"\pgfsys@transformshift{-%din}{0in}" % repx)
                _writeln(self.fh, r"\pgfsys@transformshift{0in}{1in}")

            _writeln(self.fh, r"\end{pgfscope}")

    def _print_pgf_clip(self, gc):
        f = 1. / self.dpi
        # check for clip box
        bbox = gc.get_clip_rectangle()
        if bbox:
            p1, p2 = bbox.get_points()
            w, h = p2 - p1
            coords = p1[0] * f, p1[1] * f, w * f, h * f
            _writeln(self.fh,
                     r"\pgfpathrectangle"
                     r"{\pgfqpoint{%fin}{%fin}}{\pgfqpoint{%fin}{%fin}}"
                     % coords)
            _writeln(self.fh, r"\pgfusepath{clip}")

        # check for clip path
        clippath, clippath_trans = gc.get_clip_path()
        if clippath is not None:
            self._print_pgf_path(gc, clippath, clippath_trans)
            _writeln(self.fh, r"\pgfusepath{clip}")

    def _print_pgf_path_styles(self, gc, rgbFace):
        # cap style
        capstyles = {"butt": r"\pgfsetbuttcap",
                     "round": r"\pgfsetroundcap",
                     "projecting": r"\pgfsetrectcap"}
        _writeln(self.fh, capstyles[gc.get_capstyle()])

        # join style
        joinstyles = {"miter": r"\pgfsetmiterjoin",
                      "round": r"\pgfsetroundjoin",
                      "bevel": r"\pgfsetbeveljoin"}
        _writeln(self.fh, joinstyles[gc.get_joinstyle()])

        # filling
        has_fill = rgbFace is not None

        if gc.get_forced_alpha():
            fillopacity = strokeopacity = gc.get_alpha()
        else:
            strokeopacity = gc.get_rgb()[3]
            fillopacity = rgbFace[3] if has_fill and len(rgbFace) > 3 else 1.0

        if has_fill:
            _writeln(self.fh,
                     r"\definecolor{currentfill}{rgb}{%f,%f,%f}"
                     % tuple(rgbFace[:3]))
            _writeln(self.fh, r"\pgfsetfillcolor{currentfill}")
        if has_fill and fillopacity != 1.0:
            _writeln(self.fh, r"\pgfsetfillopacity{%f}" % fillopacity)

        # linewidth and color
        lw = gc.get_linewidth() * mpl_pt_to_in * latex_in_to_pt
        stroke_rgba = gc.get_rgb()
        _writeln(self.fh, r"\pgfsetlinewidth{%fpt}" % lw)
        _writeln(self.fh,
                 r"\definecolor{currentstroke}{rgb}{%f,%f,%f}"
                 % stroke_rgba[:3])
        _writeln(self.fh, r"\pgfsetstrokecolor{currentstroke}")
        if strokeopacity != 1.0:
            _writeln(self.fh, r"\pgfsetstrokeopacity{%f}" % strokeopacity)

        # line style
        dash_offset, dash_list = gc.get_dashes()
        if dash_list is None:
            _writeln(self.fh, r"\pgfsetdash{}{0pt}")
        else:
            _writeln(self.fh,
                     r"\pgfsetdash{%s}{%fpt}"
                     % ("".join(r"{%fpt}" % dash for dash in dash_list),
                        dash_offset))

    def _print_pgf_path(self, gc, path, transform, rgbFace=None):
        f = 1. / self.dpi
        # check for clip box / ignore clip for filled paths
        bbox = gc.get_clip_rectangle() if gc else None
        maxcoord = 16383 / 72.27 * self.dpi  # Max dimensions in LaTeX.
        if bbox and (rgbFace is None):
            p1, p2 = bbox.get_points()
            clip = (max(p1[0], -maxcoord), max(p1[1], -maxcoord),
                    min(p2[0], maxcoord), min(p2[1], maxcoord))
        else:
            clip = (-maxcoord, -maxcoord, maxcoord, maxcoord)
        # build path
        for points, code in path.iter_segments(transform, clip=clip):
            if code == Path.MOVETO:
                x, y = tuple(points)
                _writeln(self.fh,
                         r"\pgfpathmoveto{\pgfqpoint{%fin}{%fin}}" %
                         (f * x, f * y))
            elif code == Path.CLOSEPOLY:
                _writeln(self.fh, r"\pgfpathclose")
            elif code == Path.LINETO:
                x, y = tuple(points)
                _writeln(self.fh,
                         r"\pgfpathlineto{\pgfqpoint{%fin}{%fin}}" %
                         (f * x, f * y))
            elif code == Path.CURVE3:
                cx, cy, px, py = tuple(points)
                coords = cx * f, cy * f, px * f, py * f
                _writeln(self.fh,
                         r"\pgfpathquadraticcurveto"
                         r"{\pgfqpoint{%fin}{%fin}}{\pgfqpoint{%fin}{%fin}}"
                         % coords)
            elif code == Path.CURVE4:
                c1x, c1y, c2x, c2y, px, py = tuple(points)
                coords = c1x * f, c1y * f, c2x * f, c2y * f, px * f, py * f
                _writeln(self.fh,
                         r"\pgfpathcurveto"
                         r"{\pgfqpoint{%fin}{%fin}}"
                         r"{\pgfqpoint{%fin}{%fin}}"
                         r"{\pgfqpoint{%fin}{%fin}}"
                         % coords)

        # apply pgf decorators
        sketch_params = gc.get_sketch_params() if gc else None
        if sketch_params is not None:
            # Only "length" directly maps to "segment length" in PGF's API.
            # PGF uses "amplitude" to pass the combined deviation in both x-
            # and y-direction, while matplotlib only varies the length of the
            # wiggle along the line ("randomness" and "length" parameters)
            # and has a separate "scale" argument for the amplitude.
            # -> Use "randomness" as PRNG seed to allow the user to force the
            # same shape on multiple sketched lines
            scale, length, randomness = sketch_params
            if scale is not None:
                # make matplotlib and PGF rendering visually similar
                length *= 0.5
                scale *= 2
                # PGF guarantees that repeated loading is a no-op
                _writeln(self.fh, r"\usepgfmodule{decorations}")
                _writeln(self.fh, r"\usepgflibrary{decorations.pathmorphing}")
                _writeln(self.fh, r"\pgfkeys{/pgf/decoration/.cd, "
                         f"segment length = {(length * f):f}in, "
                         f"amplitude = {(scale * f):f}in}}")
                _writeln(self.fh, f"\\pgfmathsetseed{{{int(randomness)}}}")
                _writeln(self.fh, r"\pgfdecoratecurrentpath{random steps}")

    def _pgf_path_draw(self, stroke=True, fill=False):
        actions = []
        if stroke:
            actions.append("stroke")
        if fill:
            actions.append("fill")
        _writeln(self.fh, r"\pgfusepath{%s}" % ",".join(actions))

    def option_scale_image(self):
        # docstring inherited
        return True

    def option_image_nocomposite(self):
        # docstring inherited
        return not mpl.rcParams['image.composite_image']

    def draw_image(self, gc, x, y, im, transform=None):
        # docstring inherited

        h, w = im.shape[:2]
        if w == 0 or h == 0:
            return

        if not os.path.exists(getattr(self.fh, "name", "")):
            raise ValueError(
                "streamed pgf-code does not support raster graphics, consider "
                "using the pgf-to-pdf option")

        # save the images to png files
        path = pathlib.Path(self.fh.name)
        fname_img = "%s-img%d.png" % (path.stem, self.image_counter)
        Image.fromarray(im[::-1]).save(path.parent / fname_img)
        self.image_counter += 1

        # reference the image in the pgf picture
        _writeln(self.fh, r"\begin{pgfscope}")
        self._print_pgf_clip(gc)
        f = 1. / self.dpi  # from display coords to inch
        if transform is None:
            _writeln(self.fh,
                     r"\pgfsys@transformshift{%fin}{%fin}" % (x * f, y * f))
            w, h = w * f, h * f
        else:
            tr1, tr2, tr3, tr4, tr5, tr6 = transform.frozen().to_values()
            _writeln(self.fh,
                     r"\pgfsys@transformcm{%f}{%f}{%f}{%f}{%fin}{%fin}" %
                     (tr1 * f, tr2 * f, tr3 * f, tr4 * f,
                      (tr5 + x) * f, (tr6 + y) * f))
            w = h = 1  # scale is already included in the transform
        interp = str(transform is None).lower()  # interpolation in PDF reader
        _writeln(self.fh,
                 r"\pgftext[left,bottom]"
                 r"{%s[interpolate=%s,width=%fin,height=%fin]{%s}}" %
                 (_get_image_inclusion_command(),
                  interp, w, h, fname_img))
        _writeln(self.fh, r"\end{pgfscope}")

    def draw_tex(self, gc, x, y, s, prop, angle, ismath="TeX", mtext=None):
        # docstring inherited
        self.draw_text(gc, x, y, s, prop, angle, ismath, mtext)

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # docstring inherited

        # prepare string for tex
        s = _escape_and_apply_props(s, prop)

        _writeln(self.fh, r"\begin{pgfscope}")

        alpha = gc.get_alpha()
        if alpha != 1.0:
            _writeln(self.fh, r"\pgfsetfillopacity{%f}" % alpha)
            _writeln(self.fh, r"\pgfsetstrokeopacity{%f}" % alpha)
        rgb = tuple(gc.get_rgb())[:3]
        _writeln(self.fh, r"\definecolor{textcolor}{rgb}{%f,%f,%f}" % rgb)
        _writeln(self.fh, r"\pgfsetstrokecolor{textcolor}")
        _writeln(self.fh, r"\pgfsetfillcolor{textcolor}")
        s = r"\color{textcolor}" + s

        dpi = self.figure.dpi
        text_args = []
        if mtext and (
                (angle == 0 or
                 mtext.get_rotation_mode() == "anchor") and
                mtext.get_verticalalignment() != "center_baseline"):
            # if text anchoring can be supported, get the original coordinates
            # and add alignment information
            pos = mtext.get_unitless_position()
            x, y = mtext.get_transform().transform(pos)
            halign = {"left": "left", "right": "right", "center": ""}
            valign = {"top": "top", "bottom": "bottom",
                      "baseline": "base", "center": ""}
            text_args.extend([
                f"x={x/dpi:f}in",
                f"y={y/dpi:f}in",
                halign[mtext.get_horizontalalignment()],
                valign[mtext.get_verticalalignment()],
            ])
        else:
            # if not, use the text layout provided by Matplotlib.
            text_args.append(f"x={x/dpi:f}in, y={y/dpi:f}in, left, base")

        if angle != 0:
            text_args.append("rotate=%f" % angle)

        _writeln(self.fh, r"\pgftext[%s]{%s}" % (",".join(text_args), s))
        _writeln(self.fh, r"\end{pgfscope}")

    def get_text_width_height_descent(self, s, prop, ismath):
        # docstring inherited
        # get text metrics in units of latex pt, convert to display units
        w, h, d = (LatexManager._get_cached_or_new()
                   .get_width_height_descent(s, prop))
        # TODO: this should be latex_pt_to_in instead of mpl_pt_to_in
        # but having a little bit more space around the text looks better,
        # plus the bounding box reported by LaTeX is VERY narrow
        f = mpl_pt_to_in * self.dpi
        return w * f, h * f, d * f

    def flipy(self):
        # docstring inherited
        return False

    def get_canvas_width_height(self):
        # docstring inherited
        return (self.figure.get_figwidth() * self.dpi,
                self.figure.get_figheight() * self.dpi)

    def points_to_pixels(self, points):
        # docstring inherited
        return points * mpl_pt_to_in * self.dpi
