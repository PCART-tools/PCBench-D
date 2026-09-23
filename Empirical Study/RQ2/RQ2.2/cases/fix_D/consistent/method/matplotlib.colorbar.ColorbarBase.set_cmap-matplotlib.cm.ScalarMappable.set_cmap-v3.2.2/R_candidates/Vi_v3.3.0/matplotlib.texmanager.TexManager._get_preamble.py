    def _get_preamble(self):
        return "\n".join([
            r"\documentclass{article}",
            # Pass-through \mathdefault, which is used in non-usetex mode to
            # use the default text font but was historically suppressed in
            # usetex mode.
            r"\newcommand{\mathdefault}[1]{#1}",
            self._font_preamble,
            r"\usepackage[utf8]{inputenc}",
            r"\DeclareUnicodeCharacter{2212}{\ensuremath{-}}",
            # geometry is loaded before the custom preamble as convert_psfrags
            # relies on a custom preamble to change the geometry.
            r"\usepackage[papersize=72in,body=70in,margin=1in]{geometry}",
            self.get_custom_preamble(),
            # textcomp is loaded last (if not already loaded by the custom
            # preamble) in order not to clash with custom packages (e.g.
            # newtxtext) which load it with different options.
            r"\makeatletter"
            r"\@ifpackageloaded{textcomp}{}{\usepackage{textcomp}}"
            r"\makeatother",
        ])
