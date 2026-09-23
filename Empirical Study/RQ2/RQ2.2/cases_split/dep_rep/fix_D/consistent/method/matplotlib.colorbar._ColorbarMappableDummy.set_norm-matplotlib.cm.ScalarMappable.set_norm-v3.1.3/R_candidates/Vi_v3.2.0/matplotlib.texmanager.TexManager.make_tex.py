    def make_tex(self, tex, fontsize):
        """
        Generate a tex file to render the tex string at a specific font size.

        Return the file name.
        """
        basefile = self.get_basefile(tex, fontsize)
        texfile = '%s.tex' % basefile
        custom_preamble = self.get_custom_preamble()
        fontcmd = {'sans-serif': r'{\sffamily %s}',
                   'monospace': r'{\ttfamily %s}'}.get(self.font_family,
                                                       r'{\rmfamily %s}')
        tex = fontcmd % tex

        unicode_preamble = "\n".join([
            r"\usepackage[utf8]{inputenc}",
            r"\DeclareUnicodeCharacter{2212}{\ensuremath{-}}",
        ]) if rcParams["text.latex.unicode"] else ""

        s = r"""
\documentclass{article}
%s
%s
%s
\usepackage[papersize={72in,72in},body={70in,70in},margin={1in,1in}]{geometry}
\pagestyle{empty}
\begin{document}
\fontsize{%f}{%f}%s
\end{document}
""" % (self._font_preamble, unicode_preamble, custom_preamble,
       fontsize, fontsize * 1.25, tex)
        with open(texfile, 'wb') as fh:
            if rcParams['text.latex.unicode']:
                fh.write(s.encode('utf8'))
            else:
                try:
                    fh.write(s.encode('ascii'))
                except UnicodeEncodeError:
                    _log.info("You are using unicode and latex, but have not "
                              "enabled the 'text.latex.unicode' rcParam.")
                    raise

        return texfile
