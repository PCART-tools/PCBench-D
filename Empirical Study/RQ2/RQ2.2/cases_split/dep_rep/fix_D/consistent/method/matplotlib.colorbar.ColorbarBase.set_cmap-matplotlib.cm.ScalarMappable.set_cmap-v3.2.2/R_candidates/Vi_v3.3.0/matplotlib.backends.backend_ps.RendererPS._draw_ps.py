    def _draw_ps(self, ps, gc, rgbFace, fill=True, stroke=True, command=None):
        """
        Emit the PostScript snippet 'ps' with all the attributes from 'gc'
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
        mightstroke = (gc.get_linewidth() > 0
                       and not _is_transparent(gc.get_rgb()))
        if not mightstroke:
            stroke = False
        if _is_transparent(rgbFace):
            fill = False
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
            write('%1.4g %1.4g %1.4g %1.4g clipbox\n'
                  % (*cliprect.size, *cliprect.p0))
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
            self.set_color(*rgbFace[:3], store=False)
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
