    def _parse(self, file):
        """
        Parse the font mapping file.

        The format is, AFAIK: texname fontname [effects and filenames]
        Effects are PostScript snippets like ".177 SlantFont",
        filenames begin with one or two less-than signs. A filename
        ending in enc is an encoding file, other filenames are font
        files. This can be overridden with a left bracket: <[foobar
        indicates an encoding file named foobar.

        There is some difference between <foo.pfb and <<bar.pfb in
        subsetting, but I have no example of << in my TeX installation.
        """
        # If the map file specifies multiple encodings for a font, we
        # follow pdfTeX in choosing the last one specified. Such
        # entries are probably mistakes but they have occurred.
        # http://tex.stackexchange.com/questions/10826/
        # http://article.gmane.org/gmane.comp.tex.pdftex/4914

        empty_re = re.compile(br'%|\s*$')
        word_re = re.compile(
            br'''(?x) (?:
                 "<\[ (?P<enc1>  [^"]+    )" | # quoted encoding marked by [
                 "<   (?P<enc2>  [^"]+.enc)" | # quoted encoding, ends in .enc
                 "<<? (?P<file1> [^"]+    )" | # quoted font file name
                 "    (?P<eff1>  [^"]+    )" | # quoted effects or font name
                 <\[  (?P<enc3>  \S+      )  | # encoding marked by [
                 <    (?P<enc4>  \S+  .enc)  | # encoding, ends in .enc
                 <<?  (?P<file2> \S+      )  | # font file name
                      (?P<eff2>  \S+      )    # effects or font name
            )''')
        effects_re = re.compile(
            br'''(?x) (?P<slant> -?[0-9]*(?:\.[0-9]+)) \s* SlantFont
                    | (?P<extend>-?[0-9]*(?:\.[0-9]+)) \s* ExtendFont''')

        lines = (line.strip()
                 for line in file
                 if not empty_re.match(line))
        for line in lines:
            effects, encoding, filename = b'', None, None
            words = word_re.finditer(line)

            # The named groups are mutually exclusive and are
            # referenced below at an estimated order of probability of
            # occurrence based on looking at my copy of pdftex.map.
            # The font names are probably unquoted:
            w = next(words)
            texname = w.group('eff2') or w.group('eff1')
            w = next(words)
            psname = w.group('eff2') or w.group('eff1')

            for w in words:
                # Any effects are almost always quoted:
                eff = w.group('eff1') or w.group('eff2')
                if eff:
                    effects = eff
                    continue
                # Encoding files usually have the .enc suffix
                # and almost never need quoting:
                enc = (w.group('enc4') or w.group('enc3') or
                       w.group('enc2') or w.group('enc1'))
                if enc:
                    if encoding is not None:
                        matplotlib.verbose.report(
                            'Multiple encodings for %s = %s'
                            % (texname, psname),
                            'debug')
                    encoding = enc
                    continue
                # File names are probably unquoted:
                filename = w.group('file2') or w.group('file1')

            effects_dict = {}
            for match in effects_re.finditer(effects):
                slant = match.group('slant')
                if slant:
                    effects_dict['slant'] = float(slant)
                else:
                    effects_dict['extend'] = float(match.group('extend'))

            self._font[texname] = PsFont(
                texname=texname, psname=psname, effects=effects_dict,
                encoding=encoding, filename=filename)
