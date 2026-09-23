    def _write_header(self, width_inches, height_inches):
        hyperref_options = ','.join(
            _metadata_to_str(k, v) for k, v in self._info_dict.items())

        latex_preamble = get_preamble()
        latex_fontspec = get_fontspec()
        latex_header = r"""\PassOptionsToPackage{{
  pdfinfo={{
    {metadata}
  }}
}}{{hyperref}}
\RequirePackage{{hyperref}}
\documentclass[12pt]{{minimal}}
\usepackage[
    paperwidth={width}in,
    paperheight={height}in,
    margin=0in
]{{geometry}}
{preamble}
{fontspec}
\usepackage{{pgf}}
\setlength{{\parindent}}{{0pt}}

\begin{{document}}%%
""".format(
            width=width_inches,
            height=height_inches,
            preamble=latex_preamble,
            fontspec=latex_fontspec,
            metadata=hyperref_options,
        )
        self._file.write(latex_header.encode('utf-8'))
