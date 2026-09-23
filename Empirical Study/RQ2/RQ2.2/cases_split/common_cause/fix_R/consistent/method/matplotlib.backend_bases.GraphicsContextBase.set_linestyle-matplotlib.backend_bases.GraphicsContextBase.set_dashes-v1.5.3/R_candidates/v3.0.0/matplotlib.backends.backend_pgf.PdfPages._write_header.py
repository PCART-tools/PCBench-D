    def _write_header(self, width_inches, height_inches):
        supported_keys = {
            'title', 'author', 'subject', 'keywords', 'creator',
            'producer', 'trapped'
        }
        infoDict = {
            'creator': 'matplotlib %s, https://matplotlib.org' % __version__,
            'producer': 'matplotlib pgf backend %s' % __version__,
        }
        metadata = {k.lower(): v for k, v in self.metadata.items()}
        infoDict.update(metadata)
        hyperref_options = ''
        for k, v in infoDict.items():
            if k not in supported_keys:
                raise ValueError(
                    'Not a supported pdf metadata field: "{}"'.format(k)
                )
            hyperref_options += 'pdf' + k + '={' + str(v) + '},'

        latex_preamble = get_preamble()
        latex_fontspec = get_fontspec()
        latex_header = r"""\PassOptionsToPackage{{
  {metadata}
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
