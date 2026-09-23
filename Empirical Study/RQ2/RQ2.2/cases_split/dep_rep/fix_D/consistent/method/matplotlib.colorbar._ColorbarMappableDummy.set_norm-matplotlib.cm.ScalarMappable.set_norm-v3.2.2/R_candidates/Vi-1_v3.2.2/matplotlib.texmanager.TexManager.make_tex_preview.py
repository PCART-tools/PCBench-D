    def make_tex_preview(self, tex, fontsize):
        """
        Generate a tex file to render the tex string at a specific font size.

        It uses the preview.sty to determine the dimension (width, height,
        descent) of the output.

        Return the file name.
        """
        basefile = self.get_basefile(tex, fontsize)
        texfile = '%s.tex' % basefile
        fontcmd = {'sans-serif': r'{\sffamily %s}',
                   'monospace': r'{\ttfamily %s}'}.get(self.font_family,
                                                       r'{\rmfamily %s}')
        tex = fontcmd % tex

        # newbox, setbox, immediate, etc. are used to find the box
        # extent of the rendered text.

        s = r"""
%s
\usepackage[active,showbox,tightpage]{preview}

%% we override the default showbox as it is treated as an error and makes
%% the exit status not zero
\def\showbox#1%%
{\immediate\write16{MatplotlibBox:(\the\ht#1+\the\dp#1)x\the\wd#1}}

\begin{document}
\begin{preview}
{\fontsize{%f}{%f}%s}
\end{preview}
\end{document}
""" % (self._get_preamble(), fontsize, fontsize * 1.25, tex)
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
