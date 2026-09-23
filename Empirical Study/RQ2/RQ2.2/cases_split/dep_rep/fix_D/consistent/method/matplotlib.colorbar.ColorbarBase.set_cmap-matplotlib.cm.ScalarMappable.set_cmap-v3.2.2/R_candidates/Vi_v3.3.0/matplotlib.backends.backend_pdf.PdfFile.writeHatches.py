    def writeHatches(self):
        hatchDict = dict()
        sidelen = 72.0
        for hatch_style, name in self.hatchPatterns.items():
            ob = self.reserveObject('hatch pattern')
            hatchDict[name] = ob
            res = {'Procsets':
                   [Name(x) for x in "PDF Text ImageB ImageC ImageI".split()]}
            self.beginStream(
                ob.id, None,
                {'Type': Name('Pattern'),
                 'PatternType': 1, 'PaintType': 1, 'TilingType': 1,
                 'BBox': [0, 0, sidelen, sidelen],
                 'XStep': sidelen, 'YStep': sidelen,
                 'Resources': res,
                 # Change origin to match Agg at top-left.
                 'Matrix': [1, 0, 0, 1, 0, self.height * 72]})

            stroke_rgb, fill_rgb, path = hatch_style
            self.output(stroke_rgb[0], stroke_rgb[1], stroke_rgb[2],
                        Op.setrgb_stroke)
            if fill_rgb is not None:
                self.output(fill_rgb[0], fill_rgb[1], fill_rgb[2],
                            Op.setrgb_nonstroke,
                            0, 0, sidelen, sidelen, Op.rectangle,
                            Op.fill)

            self.output(mpl.rcParams['hatch.linewidth'], Op.setlinewidth)

            self.output(*self.pathOperations(
                Path.hatch(path),
                Affine2D().scale(sidelen),
                simplify=False))
            self.output(Op.fill_stroke)

            self.endStream()
        self.writeObject(self.hatchObject, hatchDict)
