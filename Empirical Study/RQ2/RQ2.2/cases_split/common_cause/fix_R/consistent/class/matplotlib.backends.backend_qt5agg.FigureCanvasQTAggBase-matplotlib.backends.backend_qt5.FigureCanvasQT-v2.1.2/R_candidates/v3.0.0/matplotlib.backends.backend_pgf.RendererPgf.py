class RendererPgf(RendererBase):

    def __init__(self, figure, fh, dummy=False):
        """
        Creates a new PGF renderer that translates any drawing instruction
        into text commands to be interpreted in a latex pgfpicture environment.

        Attributes
        ----------
        figure : `matplotlib.figure.Figure`
            Matplotlib figure to initialize height, width and dpi from.
        fh : file-like
            File handle for the output of the drawing commands.

        """
        RendererBase.__init__(self)
        self.dpi = figure.dpi
        self.fh = fh
        self.figure = figure
        self.image_counter = 0

        # get LatexManager instance
        self.latexManager = LatexManagerFactory.get_latex_manager()

        if dummy:
            # dummy==True deactivate all methods
            nop = lambda *args, **kwargs: None
            for m in RendererPgf.__dict__:
                if m.startswith("draw_"):
                    self.__dict__[m] = nop
        else:
            # if fh does not belong to a filename, deactivate draw_image
            if not hasattr(fh, 'name') or not os.path.exists(fh.name):
                warnings.warn("streamed pgf-code does not support raster "
                              "graphics, consider using the pgf-to-pdf option",
                              UserWarning, stacklevel=2)
                self.__dict__["draw_image"] = lambda *args, **kwargs: None

    def draw_markers(self, gc, marker_path, marker_trans, path, trans,
                     rgbFace=None):
        writeln(self.fh, r"\begin{pgfscope}")

        # convert from display units to in
        f = 1. / self.dpi

        # set style and clip
        self._print_pgf_clip(gc)
        self._print_pgf_path_styles(gc, rgbFace)

        # build marker definition
        bl, tr = marker_path.get_extents(marker_trans).get_points()
        coords = bl[0] * f, bl[1] * f, tr[0] * f, tr[1] * f
        writeln(self.fh,
                r"\pgfsys@defobject{currentmarker}"
                r"{\pgfqpoint{%fin}{%fin}}{\pgfqpoint{%fin}{%fin}}{" % coords)
        self._print_pgf_path(None, marker_path, marker_trans)
        self._pgf_path_draw(stroke=gc.get_linewidth() != 0.0,
                            fill=rgbFace is not None)
        writeln(self.fh, r"}")

        # draw marker for each vertex
        for point, code in path.iter_segments(trans, simplify=False):
            x, y = point[0] * f, point[1] * f
            writeln(self.fh, r"\begin{pgfscope}")
            writeln(self.fh, r"\pgfsys@transformshift{%fin}{%fin}" % (x, y))
            writeln(self.fh, r"\pgfsys@useobject{currentmarker}{}")
            writeln(self.fh, r"\end{pgfscope}")

        writeln(self.fh, r"\end{pgfscope}")

    def draw_path(self, gc, path, transform, rgbFace=None):
        writeln(self.fh, r"\begin{pgfscope}")
        # draw the path
        self._print_pgf_clip(gc)
        self._print_pgf_path_styles(gc, rgbFace)
        self._print_pgf_path(gc, path, transform, rgbFace)
        self._pgf_path_draw(stroke=gc.get_linewidth() != 0.0,
                            fill=rgbFace is not None)
        writeln(self.fh, r"\end{pgfscope}")

        # if present, draw pattern on top
        if gc.get_hatch():
            writeln(self.fh, r"\begin{pgfscope}")
            self._print_pgf_path_styles(gc, rgbFace)

            # combine clip and path for clipping
            self._print_pgf_clip(gc)
            self._print_pgf_path(gc, path, transform, rgbFace)
            writeln(self.fh, r"\pgfusepath{clip}")

            # build pattern definition
            writeln(self.fh,
                    r"\pgfsys@defobject{currentpattern}"
                    r"{\pgfqpoint{0in}{0in}}{\pgfqpoint{1in}{1in}}{")
            writeln(self.fh, r"\begin{pgfscope}")
            writeln(self.fh,
                    r"\pgfpathrectangle"
                    r"{\pgfqpoint{0in}{0in}}{\pgfqpoint{1in}{1in}}")
            writeln(self.fh, r"\pgfusepath{clip}")
            scale = mpl.transforms.Affine2D().scale(self.dpi)
            self._print_pgf_path(None, gc.get_hatch_path(), scale)
            self._pgf_path_draw(stroke=True)
            writeln(self.fh, r"\end{pgfscope}")
            writeln(self.fh, r"}")
            # repeat pattern, filling the bounding rect of the path
            f = 1. / self.dpi
            (xmin, ymin), (xmax, ymax) = \
                path.get_extents(transform).get_points()
            xmin, xmax = f * xmin, f * xmax
            ymin, ymax = f * ymin, f * ymax
            repx, repy = int(math.ceil(xmax-xmin)), int(math.ceil(ymax-ymin))
            writeln(self.fh,
                    r"\pgfsys@transformshift{%fin}{%fin}" % (xmin, ymin))
            for iy in range(repy):
                for ix in range(repx):
                    writeln(self.fh, r"\pgfsys@useobject{currentpattern}{}")
                    writeln(self.fh, r"\pgfsys@transformshift{1in}{0in}")
                writeln(self.fh, r"\pgfsys@transformshift{-%din}{0in}" % repx)
                writeln(self.fh, r"\pgfsys@transformshift{0in}{1in}")

            writeln(self.fh, r"\end{pgfscope}")

    def _print_pgf_clip(self, gc):
        f = 1. / self.dpi
        # check for clip box
        bbox = gc.get_clip_rectangle()
        if bbox:
            p1, p2 = bbox.get_points()
            w, h = p2 - p1
            coords = p1[0] * f, p1[1] * f, w * f, h * f
            writeln(self.fh,
                    r"\pgfpathrectangle"
                    r"{\pgfqpoint{%fin}{%fin}}{\pgfqpoint{%fin}{%fin}}"
                    % coords)
            writeln(self.fh, r"\pgfusepath{clip}")

        # check for clip path
        clippath, clippath_trans = gc.get_clip_path()
        if clippath is not None:
            self._print_pgf_path(gc, clippath, clippath_trans)
            writeln(self.fh, r"\pgfusepath{clip}")

    def _print_pgf_path_styles(self, gc, rgbFace):
        # cap style
        capstyles = {"butt": r"\pgfsetbuttcap",
                     "round": r"\pgfsetroundcap",
                     "projecting": r"\pgfsetrectcap"}
        writeln(self.fh, capstyles[gc.get_capstyle()])

        # join style
        joinstyles = {"miter": r"\pgfsetmiterjoin",
                      "round": r"\pgfsetroundjoin",
                      "bevel": r"\pgfsetbeveljoin"}
        writeln(self.fh, joinstyles[gc.get_joinstyle()])

        # filling
        has_fill = rgbFace is not None

        if gc.get_forced_alpha():
            fillopacity = strokeopacity = gc.get_alpha()
        else:
            strokeopacity = gc.get_rgb()[3]
            fillopacity = rgbFace[3] if has_fill and len(rgbFace) > 3 else 1.0

        if has_fill:
            writeln(self.fh,
                    r"\definecolor{currentfill}{rgb}{%f,%f,%f}"
                    % tuple(rgbFace[:3]))
            writeln(self.fh, r"\pgfsetfillcolor{currentfill}")
        if has_fill and fillopacity != 1.0:
            writeln(self.fh, r"\pgfsetfillopacity{%f}" % fillopacity)

        # linewidth and color
        lw = gc.get_linewidth() * mpl_pt_to_in * latex_in_to_pt
        stroke_rgba = gc.get_rgb()
        writeln(self.fh, r"\pgfsetlinewidth{%fpt}" % lw)
        writeln(self.fh,
                r"\definecolor{currentstroke}{rgb}{%f,%f,%f}"
                % stroke_rgba[:3])
        writeln(self.fh, r"\pgfsetstrokecolor{currentstroke}")
        if strokeopacity != 1.0:
            writeln(self.fh, r"\pgfsetstrokeopacity{%f}" % strokeopacity)

        # line style
        dash_offset, dash_list = gc.get_dashes()
        if dash_list is None:
            writeln(self.fh, r"\pgfsetdash{}{0pt}")
        else:
            writeln(self.fh,
                    r"\pgfsetdash{%s}{%fpt}"
                    % ("".join(r"{%fpt}" % dash for dash in dash_list),
                       dash_offset))

    def _print_pgf_path(self, gc, path, transform, rgbFace=None):
        f = 1. / self.dpi
        # check for clip box / ignore clip for filled paths
        bbox = gc.get_clip_rectangle() if gc else None
        if bbox and (rgbFace is None):
            p1, p2 = bbox.get_points()
            clip = (p1[0], p1[1], p2[0], p2[1])
        else:
            clip = None
        # build path
        for points, code in path.iter_segments(transform, clip=clip):
            if code == Path.MOVETO:
                x, y = tuple(points)
                writeln(self.fh,
                        r"\pgfpathmoveto{\pgfqpoint{%fin}{%fin}}" %
                        (f * x, f * y))
            elif code == Path.CLOSEPOLY:
                writeln(self.fh, r"\pgfpathclose")
            elif code == Path.LINETO:
                x, y = tuple(points)
                writeln(self.fh,
                        r"\pgfpathlineto{\pgfqpoint{%fin}{%fin}}" %
                        (f * x, f * y))
            elif code == Path.CURVE3:
                cx, cy, px, py = tuple(points)
                coords = cx * f, cy * f, px * f, py * f
                writeln(self.fh,
                        r"\pgfpathquadraticcurveto"
                        r"{\pgfqpoint{%fin}{%fin}}{\pgfqpoint{%fin}{%fin}}"
                        % coords)
            elif code == Path.CURVE4:
                c1x, c1y, c2x, c2y, px, py = tuple(points)
                coords = c1x * f, c1y * f, c2x * f, c2y * f, px * f, py * f
                writeln(self.fh,
                        r"\pgfpathcurveto"
                        r"{\pgfqpoint{%fin}{%fin}}"
                        r"{\pgfqpoint{%fin}{%fin}}"
                        r"{\pgfqpoint{%fin}{%fin}}"
                        % coords)

    def _pgf_path_draw(self, stroke=True, fill=False):
        actions = []
        if stroke:
            actions.append("stroke")
        if fill:
            actions.append("fill")
        writeln(self.fh, r"\pgfusepath{%s}" % ",".join(actions))

    def option_scale_image(self):
        """
        pgf backend supports affine transform of image.
        """
        return True

    def option_image_nocomposite(self):
        """
        return whether to generate a composite image from multiple images on
        a set of axes
        """
        return not rcParams['image.composite_image']

    def draw_image(self, gc, x, y, im, transform=None):
        h, w = im.shape[:2]
        if w == 0 or h == 0:
            return

        # save the images to png files
        path = os.path.dirname(self.fh.name)
        fname = os.path.splitext(os.path.basename(self.fh.name))[0]
        fname_img = "%s-img%d.png" % (fname, self.image_counter)
        self.image_counter += 1
        _png.write_png(im[::-1], os.path.join(path, fname_img))

        # reference the image in the pgf picture
        writeln(self.fh, r"\begin{pgfscope}")
        self._print_pgf_clip(gc)
        f = 1. / self.dpi  # from display coords to inch
        if transform is None:
            writeln(self.fh,
                    r"\pgfsys@transformshift{%fin}{%fin}" % (x * f, y * f))
            w, h = w * f, h * f
        else:
            tr1, tr2, tr3, tr4, tr5, tr6 = transform.frozen().to_values()
            writeln(self.fh,
                    r"\pgfsys@transformcm{%f}{%f}{%f}{%f}{%fin}{%fin}" %
                    (tr1 * f, tr2 * f, tr3 * f, tr4 * f,
                     (tr5 + x) * f, (tr6 + y) * f))
            w = h = 1  # scale is already included in the transform
        interp = str(transform is None).lower()  # interpolation in PDF reader
        writeln(self.fh,
                r"\pgftext[left,bottom]"
                r"{\pgfimage[interpolate=%s,width=%fin,height=%fin]{%s}}" %
                (interp, w, h, fname_img))
        writeln(self.fh, r"\end{pgfscope}")

    def draw_tex(self, gc, x, y, s, prop, angle, ismath="TeX!", mtext=None):
        self.draw_text(gc, x, y, s, prop, angle, ismath, mtext)

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        # prepare string for tex
        s = common_texification(s)
        prop_cmds = _font_properties_str(prop)
        s = r"%s %s" % (prop_cmds, s)


        writeln(self.fh, r"\begin{pgfscope}")

        alpha = gc.get_alpha()
        if alpha != 1.0:
            writeln(self.fh, r"\pgfsetfillopacity{%f}" % alpha)
            writeln(self.fh, r"\pgfsetstrokeopacity{%f}" % alpha)
        rgb = tuple(gc.get_rgb())[:3]
        writeln(self.fh, r"\definecolor{textcolor}{rgb}{%f,%f,%f}" % rgb)
        writeln(self.fh, r"\pgfsetstrokecolor{textcolor}")
        writeln(self.fh, r"\pgfsetfillcolor{textcolor}")
        s = r"\color{textcolor}" + s

        f = 1.0 / self.figure.dpi
        text_args = []
        if mtext and (
                (angle == 0 or
                 mtext.get_rotation_mode() == "anchor") and
                mtext.get_va() != "center_baseline"):
            # if text anchoring can be supported, get the original coordinates
            # and add alignment information
            pos = mtext.get_unitless_position()
            x, y = mtext.get_transform().transform_point(pos)
            text_args.append("x=%fin" % (x * f))
            text_args.append("y=%fin" % (y * f))

            halign = {"left": "left", "right": "right", "center": ""}
            valign = {"top": "top", "bottom": "bottom",
                      "baseline": "base", "center": ""}
            text_args.append(halign[mtext.get_ha()])
            text_args.append(valign[mtext.get_va()])
        else:
            # if not, use the text layout provided by matplotlib
            text_args.append("x=%fin" % (x * f))
            text_args.append("y=%fin" % (y * f))
            text_args.append("left")
            text_args.append("base")

        if angle != 0:
            text_args.append("rotate=%f" % angle)

        writeln(self.fh, r"\pgftext[%s]{%s}" % (",".join(text_args), s))
        writeln(self.fh, r"\end{pgfscope}")

    def get_text_width_height_descent(self, s, prop, ismath):
        # check if the math is supposed to be displaystyled
        s = common_texification(s)

        # get text metrics in units of latex pt, convert to display units
        w, h, d = self.latexManager.get_width_height_descent(s, prop)
        # TODO: this should be latex_pt_to_in instead of mpl_pt_to_in
        # but having a little bit more space around the text looks better,
        # plus the bounding box reported by LaTeX is VERY narrow
        f = mpl_pt_to_in * self.dpi
        return w * f, h * f, d * f

    def flipy(self):
        return False

    def get_canvas_width_height(self):
        return self.figure.get_figwidth(), self.figure.get_figheight()

    def points_to_pixels(self, points):
        return points * mpl_pt_to_in * self.dpi

    def new_gc(self):
        return GraphicsContextPgf()
