    @_check_savefig_extra_args
    def _print_pgf_to_fh(self, fh, *, bbox_inches_restore=None):

        header_text = """%% Creator: Matplotlib, PGF backend
%%
%% To include the figure in your LaTeX document, write
%%   \\input{<filename>.pgf}
%%
%% Make sure the required packages are loaded in your preamble
%%   \\usepackage{pgf}
%%
%% Also ensure that all the required font packages are loaded; for instance,
%% the lmodern package is sometimes necessary when using math font.
%%   \\usepackage{lmodern}
%%
%% Figures using additional raster images can only be included by \\input if
%% they are in the same directory as the main LaTeX file. For loading figures
%% from other directories you can use the `import` package
%%   \\usepackage{import}
%%
%% and then include the figures with
%%   \\import{<path to file>}{<filename>.pgf}
%%
"""

        # append the preamble used by the backend as a comment for debugging
        header_info_preamble = ["%% Matplotlib used the following preamble"]
        for line in get_preamble().splitlines():
            header_info_preamble.append("%%   " + line)
        for line in get_fontspec().splitlines():
            header_info_preamble.append("%%   " + line)
        header_info_preamble.append("%%")
        header_info_preamble = "\n".join(header_info_preamble)

        # get figure size in inch
        w, h = self.figure.get_figwidth(), self.figure.get_figheight()
        dpi = self.figure.get_dpi()

        # create pgfpicture environment and write the pgf code
        fh.write(header_text)
        fh.write(header_info_preamble)
        fh.write("\n")
        writeln(fh, r"\begingroup")
        writeln(fh, r"\makeatletter")
        writeln(fh, r"\begin{pgfpicture}")
        writeln(fh,
                r"\pgfpathrectangle{\pgfpointorigin}{\pgfqpoint{%fin}{%fin}}"
                % (w, h))
        writeln(fh, r"\pgfusepath{use as bounding box, clip}")
        renderer = MixedModeRenderer(self.figure, w, h, dpi,
                                     RendererPgf(self.figure, fh),
                                     bbox_inches_restore=bbox_inches_restore)
        self.figure.draw(renderer)

        # end the pgfpicture environment
        writeln(fh, r"\end{pgfpicture}")
        writeln(fh, r"\makeatother")
        writeln(fh, r"\endgroup")
