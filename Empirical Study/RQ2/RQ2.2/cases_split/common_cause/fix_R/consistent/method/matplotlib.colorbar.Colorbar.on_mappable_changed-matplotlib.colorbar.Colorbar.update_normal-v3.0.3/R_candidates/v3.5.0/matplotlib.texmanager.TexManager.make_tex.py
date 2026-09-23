    def make_tex(self, tex, fontsize):
        """
        Generate a tex file to render the tex string at a specific font size.

        Return the file name.
        """
        basefile = self.get_basefile(tex, fontsize)
        texfile = '%s.tex' % basefile
        fontcmd = {'sans-serif': r'{\sffamily %s}',
                   'monospace': r'{\ttfamily %s}'}.get(self._font_family,
                                                       r'{\rmfamily %s}')

        Path(texfile).write_text(
            r"""
%s
\pagestyle{empty}
\begin{document}
%% The empty hbox ensures that a page is printed even for empty inputs, except
%% when using psfrag which gets confused by it.
\fontsize{%f}{%f}%%
\ifdefined\psfrag\else\hbox{}\fi%%
%s
\end{document}
""" % (self._get_preamble(), fontsize, fontsize * 1.25, fontcmd % tex),
            encoding='utf-8')

        return texfile
