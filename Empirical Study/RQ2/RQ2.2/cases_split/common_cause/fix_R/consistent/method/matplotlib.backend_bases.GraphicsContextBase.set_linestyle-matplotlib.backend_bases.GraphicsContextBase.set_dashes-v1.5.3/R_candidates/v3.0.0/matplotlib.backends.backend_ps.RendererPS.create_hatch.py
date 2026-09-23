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
