    def make_tex(self, tex, fontsize):
        """
        Generate a tex file to render the tex string at a specific font size.

        Return the file name.
        """
        basefile = self.get_basefile(tex, fontsize)
        texfile = '%s.tex' % basefile
        fontcmd = {'sans-serif': r'{\sffamily %s}',
                   'monospace': r'{\ttfamily %s}'}.get(self.font_family,
                                                       r'{\rmfamily %s}')
        tex = fontcmd % tex

        s = r"""
%s
\pagestyle{empty}
\begin{document}
%% The empty hbox ensures that a page is printed even for empty inputs, except
%% when using psfrag which gets confused by it.
\fontsize{%f}{%f}%%
\ifdefined\psfrag\else\hbox{}\fi%%
%s
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
