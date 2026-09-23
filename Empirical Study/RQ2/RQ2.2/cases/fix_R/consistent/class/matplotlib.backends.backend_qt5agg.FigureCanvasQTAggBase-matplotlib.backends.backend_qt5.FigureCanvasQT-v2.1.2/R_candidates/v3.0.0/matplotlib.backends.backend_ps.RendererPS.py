class RendererPS(RendererBase):
    """
    The renderer handles all the drawing primitives using a graphics
    context instance that controls the colors/styles.
    """

    afmfontd = maxdict(50)

    def __init__(self, width, height, pswriter, imagedpi=72):
        """
        Although postscript itself is dpi independent, we need to
        imform the image code about a requested dpi to generate high
        res images and them scale them before embeddin them
        """
        RendererBase.__init__(self)
        self.width = width
        self.height = height
        self._pswriter = pswriter
        if rcParams['text.usetex']:
            self.textcnt = 0
            self.psfrag = []
        self.imagedpi = imagedpi

        # current renderer state (None=uninitialised)
        self.color = None
        self.linewidth = None
        self.linejoin = None
        self.linecap = None
        self.linedash = None
        self.fontname = None
        self.fontsize = None
        self._hatches = {}
        self.image_magnification = imagedpi/72.0
        self._clip_paths = {}
        self._path_collection_id = 0

        self.used_characters = {}
        self.mathtext_parser = MathTextParser("PS")

        self._afm_font_dir = os.path.join(
            rcParams['datapath'], 'fonts', 'afm')

    def track_characters(self, font, s):
        """Keeps track of which characters are required from
        each font."""
        realpath, stat_key = get_realpath_and_stat(font.fname)
        used_characters = self.used_characters.setdefault(
            stat_key, (realpath, set()))
        used_characters[1].update(map(ord, s))

    def merge_used_characters(self, other):
        for stat_key, (realpath, charset) in other.items():
            used_characters = self.used_characters.setdefault(
                stat_key, (realpath, set()))
            used_characters[1].update(charset)

    def set_color(self, r, g, b, store=1):
        if (r,g,b) != self.color:
            if r==g and r==b:
                self._pswriter.write("%1.3f setgray\n"%r)
            else:
                self._pswriter.write("%1.3f %1.3f %1.3f setrgbcolor\n"%(r,g,b))
            if store: self.color = (r,g,b)

    def set_linewidth(self, linewidth, store=1):
        linewidth = float(linewidth)
        if linewidth != self.linewidth:
            self._pswriter.write("%1.3f setlinewidth\n"%linewidth)
            if store: self.linewidth = linewidth

    def set_linejoin(self, linejoin, store=1):
        if linejoin != self.linejoin:
            self._pswriter.write("%d setlinejoin\n"%linejoin)
            if store: self.linejoin = linejoin

    def set_linecap(self, linecap, store=1):
        if linecap != self.linecap:
            self._pswriter.write("%d setlinecap\n"%linecap)
            if store: self.linecap = linecap

    def set_linedash(self, offset, seq, store=1):
        if self.linedash is not None:
            oldo, oldseq = self.linedash
            if np.array_equal(seq, oldseq) and oldo == offset:
                return

        if seq is not None and len(seq):
            s="[%s] %d setdash\n"%(_nums_to_str(*seq), offset)
            self._pswriter.write(s)
        else:
            self._pswriter.write("[] 0 setdash\n")
        if store:
            self.linedash = (offset, seq)

    def set_font(self, fontname, fontsize, store=1):
        if rcParams['ps.useafm']:
            return
        if (fontname, fontsize) != (self.fontname,self.fontsize):
            out = ("/%s findfont\n"
                   "%1.3f scalefont\n"
                   "setfont\n" % (fontname, fontsize))
            self._pswriter.write(out)
            if store:
                self.fontname = fontname
                self.fontsize = fontsize

    def create_hatch(self, hatch):
        sidelen = 72
        if hatch in self._hatches:
            return self._hatches[hatch]
        name = 'H%d' % len(self._hatches)
        linewidth = rcParams['hatch.linewidth']
        pageheight = self.height * 72
        self._pswriter.write("""\
  << /PatternType 1
     /PaintType 2
     /TilingType 2
     /BBox[0 0 %(sidelen)d %(sidelen)d]
     /XStep %(sidelen)d
     /YStep %(sidelen)d

     /PaintProc {
        pop
        %(linewidth)f setlinewidth
""" % locals())
        self._pswriter.write(
            self._convert_path(Path.hatch(hatch), Affine2D().scale(sidelen),
                               simplify=False))
        self._pswriter.write("""\
        fill
        stroke
     } bind
   >>
   matrix
   0.0 %(pageheight)f translate
   makepattern
   /%(name)s exch def
""" % locals())
        self._hatches[hatch] = name
        return name

    def get_canvas_width_height(self):
        'return the canvas width and height in display coords'
        return self.width * 72.0, self.height * 72.0

    def get_text_width_height_descent(self, s, prop, ismath):
        """
        get the width and height in display coords of the string s
        with FontPropertry prop

        """
        if rcParams['text.usetex']:
            texmanager = self.get_texmanager()
            fontsize = prop.get_size_in_points()
            w, h, d = texmanager.get_text_width_height_descent(s, fontsize,
                                                               renderer=self)
            return w, h, d

        if ismath:
            width, height, descent, pswriter, used_characters = \
                self.mathtext_parser.parse(s, 72, prop)
            return width, height, descent

        if rcParams['ps.useafm']:
            if ismath: s = s[1:-1]
            font = self._get_font_afm(prop)
            l,b,w,h,d = font.get_str_bbox_and_descent(s)

            fontsize = prop.get_size_in_points()
            scale = 0.001*fontsize
            w *= scale
            h *= scale
            d *= scale
            return w, h, d

        font = self._get_font_ttf(prop)
        font.set_text(s, 0.0, flags=LOAD_NO_HINTING)
        w, h = font.get_width_height()
        w /= 64.0  # convert from subpixels
        h /= 64.0
        d = font.get_descent()
        d /= 64.0
        return w, h, d

    def flipy(self):
        'return true if small y numbers are top for renderer'
        return False

    def _get_font_afm(self, prop):
        key = hash(prop)
        font = self.afmfontd.get(key)
        if font is None:
            fname = findfont(prop, fontext='afm', directory=self._afm_font_dir)
            if fname is None:
                fname = findfont(
                    "Helvetica", fontext='afm', directory=self._afm_font_dir)
            font = self.afmfontd.get(fname)
            if font is None:
                with open(fname, 'rb') as fh:
                    font = AFM(fh)
                self.afmfontd[fname] = font
            self.afmfontd[key] = font
        return font

    def _get_font_ttf(self, prop):
        fname = findfont(prop)
        font = get_font(fname)
        font.clear()
        size = prop.get_size_in_points()
        font.set_size(size, 72.0)
        return font

    def _rgb(self, rgba):
        h, w = rgba.shape[:2]
        rgb = rgba[::-1, :, :3]
        return h, w, rgb.tostring()

    def _hex_lines(self, s, chars_per_line=128):
        s = binascii.b2a_hex(s)
        nhex = len(s)
        lines = []
        for i in range(0,nhex,chars_per_line):
            limit = min(i+chars_per_line, nhex)
            lines.append(s[i:limit])
        return lines

    def get_image_magnification(self):
        """
        Get the factor by which to magnify images passed to draw_image.
        Allows a backend to have images at a different resolution to other
        artists.
        """
        return self.image_magnification

    def option_scale_image(self):
        """
        ps backend support arbitrary scaling of image.
        """
        return True

    def option_image_nocomposite(self):
        """
        return whether to generate a composite image from multiple images on
        a set of axes
        """
        return not rcParams['image.composite_image']

    def _get_image_h_w_bits_command(self, im):
        h, w, bits = self._rgb(im)
        imagecmd = "false 3 colorimage"

        return h, w, bits, imagecmd

    def draw_image(self, gc, x, y, im, transform=None):
        """
        Draw the Image instance into the current axes; x is the
        distance in pixels from the left hand side of the canvas and y
        is the distance from bottom
        """

        h, w, bits, imagecmd = self._get_image_h_w_bits_command(im)
        hexlines = b'\n'.join(self._hex_lines(bits)).decode('ascii')

        if transform is None:
            matrix = "1 0 0 1 0 0"
            xscale = w / self.image_magnification
            yscale = h / self.image_magnification
        else:
            matrix = " ".join(map(str, transform.frozen().to_values()))
            xscale = 1.0
            yscale = 1.0

        figh = self.height * 72

        bbox = gc.get_clip_rectangle()
        clippath, clippath_trans = gc.get_clip_path()

        clip = []
        if bbox is not None:
            clipx,clipy,clipw,cliph = bbox.bounds
            clip.append('%s clipbox' % _nums_to_str(clipw, cliph, clipx, clipy))
        if clippath is not None:
            id = self._get_clip_path(clippath, clippath_trans)
            clip.append('%s' % id)
        clip = '\n'.join(clip)

        ps = """gsave
%(clip)s
%(x)s %(y)s translate
[%(matrix)s] concat
%(xscale)s %(yscale)s scale
/DataString %(w)s string def
%(w)s %(h)s 8 [ %(w)s 0 0 -%(h)s 0 %(h)s ]
{
currentfile DataString readhexstring pop
} bind %(imagecmd)s
%(hexlines)s
grestore
""" % locals()
        self._pswriter.write(ps)

    def _convert_path(self, path, transform, clip=False, simplify=None):
        if clip:
            clip = (0.0, 0.0, self.width * 72.0,
                    self.height * 72.0)
        else:
            clip = None
        return _path.convert_to_string(
            path, transform, clip, simplify, None,
            6, [b'm', b'l', b'', b'c', b'cl'], True).decode('ascii')

    def _get_clip_path(self, clippath, clippath_transform):
        key = (clippath, id(clippath_transform))
        pid = self._clip_paths.get(key)
        if pid is None:
            pid = 'c%x' % len(self._clip_paths)
            ps_cmd = ['/%s {' % pid]
            ps_cmd.append(self._convert_path(clippath, clippath_transform,
                                             simplify=False))
            ps_cmd.extend(['clip', 'newpath', '} bind def\n'])
            self._pswriter.write('\n'.join(ps_cmd))
            self._clip_paths[key] = pid
        return pid

    def draw_path(self, gc, path, transform, rgbFace=None):
        """
        Draws a Path instance using the given affine transform.
        """
        clip = rgbFace is None and gc.get_hatch_path() is None
        simplify = path.should_simplify and clip
        ps = self._convert_path(path, transform, clip=clip, simplify=simplify)
        self._draw_ps(ps, gc, rgbFace)

    def draw_markers(
            self, gc, marker_path, marker_trans, path, trans, rgbFace=None):
        """
        Draw the markers defined by path at each of the positions in x
        and y.  path coordinates are points, x and y coords will be
        transformed by the transform
        """
        if debugPS: self._pswriter.write('% draw_markers \n')

        if rgbFace:
            if len(rgbFace) == 4 and rgbFace[3] == 0:
                ps_color = None
            else:
                if rgbFace[0] == rgbFace[1] == rgbFace[2]:
                    ps_color = '%1.3f setgray' % rgbFace[0]
                else:
                    ps_color = '%1.3f %1.3f %1.3f setrgbcolor' % rgbFace[:3]

        # construct the generic marker command:
        ps_cmd = ['/o {', 'gsave', 'newpath', 'translate'] # don't want the translate to be global

        lw = gc.get_linewidth()
        alpha = (gc.get_alpha()
                 if gc.get_forced_alpha() or len(gc.get_rgb()) == 3
                 else gc.get_rgb()[3])
        stroke = lw > 0 and alpha > 0
        if stroke:
            ps_cmd.append('%.1f setlinewidth' % lw)
            jint = gc.get_joinstyle()
            ps_cmd.append('%d setlinejoin' % jint)
            cint = gc.get_capstyle()
            ps_cmd.append('%d setlinecap' % cint)

        ps_cmd.append(self._convert_path(marker_path, marker_trans,
                                         simplify=False))

        if rgbFace:
            if stroke:
                ps_cmd.append('gsave')
            if ps_color:
                ps_cmd.extend([ps_color, 'fill'])
            if stroke:
                ps_cmd.append('grestore')

        if stroke:
            ps_cmd.append('stroke')
        ps_cmd.extend(['grestore', '} bind def'])

        for vertices, code in path.iter_segments(
                trans,
                clip=(0, 0, self.width*72, self.height*72),
                simplify=False):
            if len(vertices):
                x, y = vertices[-2:]
                ps_cmd.append("%g %g o" % (x, y))

        ps = '\n'.join(ps_cmd)
        self._draw_ps(ps, gc, rgbFace, fill=False, stroke=False)

    def draw_path_collection(self, gc, master_transform, paths, all_transforms,
                             offsets, offsetTrans, facecolors, edgecolors,
                             linewidths, linestyles, antialiaseds, urls,
                             offset_position):
        # Is the optimization worth it? Rough calculation:
        # cost of emitting a path in-line is
        #     (len_path + 2) * uses_per_path
        # cost of definition+use is
        #     (len_path + 3) + 3 * uses_per_path
        len_path = len(paths[0].vertices) if len(paths) > 0 else 0
        uses_per_path = self._iter_collection_uses_per_path(
            paths, all_transforms, offsets, facecolors, edgecolors)
        should_do_optimization = \
            len_path + 3 * uses_per_path + 3 < (len_path + 2) * uses_per_path
        if not should_do_optimization:
            return RendererBase.draw_path_collection(
                self, gc, master_transform, paths, all_transforms,
                offsets, offsetTrans, facecolors, edgecolors,
                linewidths, linestyles, antialiaseds, urls,
                offset_position)

        write = self._pswriter.write

        path_codes = []
        for i, (path, transform) in enumerate(self._iter_collection_raw_paths(
            master_transform, paths, all_transforms)):
            name = 'p%x_%x' % (self._path_collection_id, i)
            ps_cmd = ['/%s {' % name,
                      'newpath', 'translate']
            ps_cmd.append(self._convert_path(path, transform, simplify=False))
            ps_cmd.extend(['} bind def\n'])
            write('\n'.join(ps_cmd))
            path_codes.append(name)

        for xo, yo, path_id, gc0, rgbFace in self._iter_collection(
            gc, master_transform, all_transforms, path_codes, offsets,
            offsetTrans, facecolors, edgecolors, linewidths, linestyles,
            antialiaseds, urls, offset_position):
            ps = "%g %g %s" % (xo, yo, path_id)
            self._draw_ps(ps, gc0, rgbFace)

        self._path_collection_id += 1

    def draw_tex(self, gc, x, y, s, prop, angle, ismath='TeX!', mtext=None):
        """
        draw a Text instance
        """
        w, h, bl = self.get_text_width_height_descent(s, prop, ismath)
        fontsize = prop.get_size_in_points()
        thetext = 'psmarker%d' % self.textcnt
        color = '%1.3f,%1.3f,%1.3f'% gc.get_rgb()[:3]
        fontcmd = {'sans-serif' : r'{\sffamily %s}',
               'monospace'  : r'{\ttfamily %s}'}.get(
                rcParams['font.family'][0], r'{\rmfamily %s}')
        s = fontcmd % s
        tex = r'\color[rgb]{%s} %s' % (color, s)

        corr = 0#w/2*(fontsize-10)/10
        if rcParams['text.latex.preview']:
            # use baseline alignment!
            pos = _nums_to_str(x-corr, y)
            self.psfrag.append(r'\psfrag{%s}[Bl][Bl][1][%f]{\fontsize{%f}{%f}%s}'%(thetext, angle, fontsize, fontsize*1.25, tex))
        else:
            # stick to the bottom alignment, but this may give incorrect baseline some times.
            pos = _nums_to_str(x-corr, y-bl)
            self.psfrag.append(r'\psfrag{%s}[bl][bl][1][%f]{\fontsize{%f}{%f}%s}'%(thetext, angle, fontsize, fontsize*1.25, tex))

        ps = """\
gsave
%(pos)s moveto
(%(thetext)s)
show
grestore
    """ % locals()

        self._pswriter.write(ps)
        self.textcnt += 1

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        """
        Draw a Text instance.
        """
        # local to avoid repeated attribute lookups
        write = self._pswriter.write
        if debugPS:
            write("% text\n")

        if len(gc.get_rgb()) == 4 and gc.get_rgb()[3] == 0:
            return  # Special handling for fully transparent.

        if ismath=='TeX':
            return self.draw_tex(gc, x, y, s, prop, angle)

        elif ismath:
            return self.draw_mathtext(gc, x, y, s, prop, angle)

        elif rcParams['ps.useafm']:
            self.set_color(*gc.get_rgb())

            font = self._get_font_afm(prop)
            fontname = font.get_fontname()
            fontsize = prop.get_size_in_points()
            scale = 0.001*fontsize

            thisx = 0
            thisy = font.get_str_bbox_and_descent(s)[4] * scale
            last_name = None
            lines = []
            for c in s:
                name = uni2type1.get(ord(c), 'question')
                try:
                    width = font.get_width_from_char_name(name)
                except KeyError:
                    name = 'question'
                    width = font.get_width_char('?')
                if last_name is not None:
                    kern = font.get_kern_dist_from_name(last_name, name)
                else:
                    kern = 0
                last_name = name
                thisx += kern * scale

                lines.append('%f %f m /%s glyphshow'%(thisx, thisy, name))

                thisx += width * scale

            thetext = "\n".join(lines)
            ps = """\
gsave
/%(fontname)s findfont
%(fontsize)s scalefont
setfont
%(x)f %(y)f translate
%(angle)f rotate
%(thetext)s
grestore
    """ % locals()
            self._pswriter.write(ps)

        else:
            font = self._get_font_ttf(prop)
            font.set_text(s, 0, flags=LOAD_NO_HINTING)
            self.track_characters(font, s)

            self.set_color(*gc.get_rgb())
            ps_name = (font.postscript_name
                       .encode('ascii', 'replace').decode('ascii'))
            self.set_font(ps_name, prop.get_size_in_points())

            lastgind = None
            lines = []
            thisx = 0
            thisy = 0
            for c in s:
                ccode = ord(c)
                gind = font.get_char_index(ccode)
                if gind is None:
                    ccode = ord('?')
                    name = '.notdef'
                    gind = 0
                else:
                    name = font.get_glyph_name(gind)
                glyph = font.load_char(ccode, flags=LOAD_NO_HINTING)

                if lastgind is not None:
                    kern = font.get_kerning(lastgind, gind, KERNING_DEFAULT)
                else:
                    kern = 0
                lastgind = gind
                thisx += kern/64.0

                lines.append('%f %f m /%s glyphshow'%(thisx, thisy, name))
                thisx += glyph.linearHoriAdvance/65536.0


            thetext = '\n'.join(lines)
            ps = """gsave
%(x)f %(y)f translate
%(angle)f rotate
%(thetext)s
grestore
""" % locals()
            self._pswriter.write(ps)

    def new_gc(self):
        return GraphicsContextPS()

    def draw_mathtext(self, gc,
        x, y, s, prop, angle):
        """
        Draw the math text using matplotlib.mathtext
        """
        if debugPS:
            self._pswriter.write("% mathtext\n")

        width, height, descent, pswriter, used_characters = \
            self.mathtext_parser.parse(s, 72, prop)
        self.merge_used_characters(used_characters)
        self.set_color(*gc.get_rgb())
        thetext = pswriter.getvalue()
        ps = """gsave
%(x)f %(y)f translate
%(angle)f rotate
%(thetext)s
grestore
""" % locals()
        self._pswriter.write(ps)

    def draw_gouraud_triangle(self, gc, points, colors, trans):
        self.draw_gouraud_triangles(gc, points.reshape((1, 3, 2)),
                                    colors.reshape((1, 3, 4)), trans)

    def draw_gouraud_triangles(self, gc, points, colors, trans):
        assert len(points) == len(colors)
        assert points.ndim == 3
        assert points.shape[1] == 3
        assert points.shape[2] == 2
        assert colors.ndim == 3
        assert colors.shape[1] == 3
        assert colors.shape[2] == 4

        shape = points.shape
        flat_points = points.reshape((shape[0] * shape[1], 2))
        flat_points = trans.transform(flat_points)
        flat_colors = colors.reshape((shape[0] * shape[1], 4))
        points_min = np.min(flat_points, axis=0) - (1 << 12)
        points_max = np.max(flat_points, axis=0) + (1 << 12)
        factor = np.ceil((2 ** 32 - 1) / (points_max - points_min))

        xmin, ymin = points_min
        xmax, ymax = points_max

        streamarr = np.empty(
            (shape[0] * shape[1],),
            dtype=[('flags', 'u1'),
                   ('points', '>u4', (2,)),
                   ('colors', 'u1', (3,))])
        streamarr['flags'] = 0
        streamarr['points'] = (flat_points - points_min) * factor
        streamarr['colors'] = flat_colors[:, :3] * 255.0

        stream = quote_ps_string(streamarr.tostring())

        self._pswriter.write("""
gsave
<< /ShadingType 4
   /ColorSpace [/DeviceRGB]
   /BitsPerCoordinate 32
   /BitsPerComponent 8
   /BitsPerFlag 8
   /AntiAlias true
   /Decode [ %(xmin)f %(xmax)f %(ymin)f %(ymax)f 0 1 0 1 0 1 ]
   /DataSource (%(stream)s)
>>
shfill
grestore
""" % locals())

    def _draw_ps(self, ps, gc, rgbFace, fill=True, stroke=True, command=None):
        """
        Emit the PostScript sniplet 'ps' with all the attributes from 'gc'
        applied.  'ps' must consist of PostScript commands to construct a path.

        The fill and/or stroke kwargs can be set to False if the
        'ps' string already includes filling and/or stroking, in
        which case _draw_ps is just supplying properties and
        clipping.
        """
        # local variable eliminates all repeated attribute lookups
        write = self._pswriter.write
        if debugPS and command:
            write("% "+command+"\n")
        mightstroke = gc.shouldstroke()
        stroke = stroke and mightstroke
        fill = (fill and rgbFace is not None and
                (len(rgbFace) <= 3 or rgbFace[3] != 0.0))
        hatch = gc.get_hatch()

        if mightstroke:
            self.set_linewidth(gc.get_linewidth())
            jint = gc.get_joinstyle()
            self.set_linejoin(jint)
            cint = gc.get_capstyle()
            self.set_linecap(cint)
            self.set_linedash(*gc.get_dashes())
            self.set_color(*gc.get_rgb()[:3])
        write('gsave\n')

        cliprect = gc.get_clip_rectangle()
        if cliprect:
            x,y,w,h=cliprect.bounds
            write('%1.4g %1.4g %1.4g %1.4g clipbox\n' % (w,h,x,y))
        clippath, clippath_trans = gc.get_clip_path()
        if clippath:
            id = self._get_clip_path(clippath, clippath_trans)
            write('%s\n' % id)

        # Jochen, is the strip necessary? - this could be a honking big string
        write(ps.strip())
        write("\n")

        if fill:
            if stroke or hatch:
                write("gsave\n")
            self.set_color(store=0, *rgbFace[:3])
            write("fill\n")
            if stroke or hatch:
                write("grestore\n")

        if hatch:
            hatch_name = self.create_hatch(hatch)
            write("gsave\n")
            write("%f %f %f " % gc.get_hatch_color()[:3])
            write("%s setpattern fill grestore\n" % hatch_name)

        if stroke:
            write("stroke\n")

        write("grestore\n")
