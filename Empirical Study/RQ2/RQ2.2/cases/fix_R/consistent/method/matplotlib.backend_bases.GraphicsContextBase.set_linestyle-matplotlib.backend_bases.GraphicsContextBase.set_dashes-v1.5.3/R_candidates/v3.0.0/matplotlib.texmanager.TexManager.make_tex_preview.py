    def make_tex_preview(self, tex, fontsize):
        """
        Generate a tex file to render the tex string at a specific font size.

        It uses the preview.sty to determine the dimension (width, height,
        descent) of the output.

        Return the file name.
        """
        basefile = self.get_basefile(tex, fontsize)
        texfile = '%s.tex' % basefile
        custom_preamble = self.get_custom_preamble()
        fontcmd = {'sans-serif': r'{\sffamily %s}',
                   'monospace': r'{\ttfamily %s}'}.get(self.font_family,
                                                       r'{\rmfamily %s}')
        tex = fontcmd % tex

        if rcParams['text.latex.unicode']:
            unicode_preamble = r"""
\usepackage[utf8]{inputenc}"""
        else:
            unicode_preamble = ''

        # newbox, setbox, immediate, etc. are used to find the box
        # extent of the rendered text.

        s = r"""
\documentclass{article}
%s
%s
%s
\usepackage[active,showbox,tightpage]{preview}
\usepackage[papersize={72in,72in},body={70in,70in},margin={1in,1in}]{geometry}

%% we override the default showbox as it is treated as an error and makes
%% the exit status not zero
\def\showbox#1%%
{\immediate\write16{MatplotlibBox:(\the\ht#1+\the\dp#1)x\the\wd#1}}

\begin{document}
\begin{preview}
{\fontsize{%f}{%f}%s}
\end{preview}
\end{document}
""" % (self._font_preamble, unicode_preamble, custom_preamble,
       fontsize, fontsize * 1.25, tex)
        with open(texfile, 'wb') as fh:
            if rcParams['text.latex.unicode']:
                fh.write(s.encode('utf8'))
            else:
                try:
                    fh.write(s.encode('ascii'))
                except UnicodeEncodeError as err:
                    _log.info("You are using unicode and latex, but have not "
                              "enabled the 'text.latex.unicode' rcParam.")
                    raise

        return texfile
