    def _write_header(self, width_inches, height_inches):
        pdfinfo = ','.join(
            _metadata_to_str(k, v) for k, v in self._info_dict.items())
        latex_header = "\n".join([
            r"\PassOptionsToPackage{pdfinfo={%s}}{hyperref}" % pdfinfo,
            r"\RequirePackage{hyperref}",
            r"\documentclass[12pt]{minimal}",
            r"\usepackage[papersize={%fin,%fin}, margin=0in]{geometry}"
            % (width_inches, height_inches),
            get_preamble(),
            get_fontspec(),
            r"\usepackage{pgf}",
            r"\setlength{\parindent}{0pt}",
            r"\begin{document}%",
        ])
        self._file.write(latex_header.encode('utf-8'))
