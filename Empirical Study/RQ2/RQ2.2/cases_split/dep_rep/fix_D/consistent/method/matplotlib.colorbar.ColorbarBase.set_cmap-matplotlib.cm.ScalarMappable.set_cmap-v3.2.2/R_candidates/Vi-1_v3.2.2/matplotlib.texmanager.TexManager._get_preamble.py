    def _get_preamble(self):
        unicode_preamble = "\n".join([
            r"\usepackage[utf8]{inputenc}",
            r"\DeclareUnicodeCharacter{2212}{\ensuremath{-}}",
        ]) if rcParams["text.latex.unicode"] else ""
        return "\n".join([
            r"\documentclass{article}",
            # Pass-through \mathdefault, which is used in non-usetex mode to
            # use the default text font but was historically suppressed in
            # usetex mode.
            r"\newcommand{\mathdefault}[1]{#1}",
            self._font_preamble,
            unicode_preamble,
            # Needs to come early so that the custom preamble can change the
            # geometry, e.g. in convert_psfrags.
            r"\usepackage[papersize=72in,body=70in,margin=1in]{geometry}",
            self.get_custom_preamble(),
        ])
