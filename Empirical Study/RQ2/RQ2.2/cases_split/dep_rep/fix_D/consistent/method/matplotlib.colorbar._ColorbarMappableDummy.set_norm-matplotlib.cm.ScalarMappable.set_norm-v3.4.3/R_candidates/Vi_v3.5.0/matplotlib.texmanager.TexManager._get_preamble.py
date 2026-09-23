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
            r"\usepackage[papersize=72in, margin=1in]{geometry}",
            self.get_custom_preamble(),
            # Use `underscore` package to take care of underscores in text
            # The [strings] option allows to use underscores in file names
            _usepackage_if_not_loaded("underscore", option="strings"),
            # Custom packages (e.g. newtxtext) may already have loaded textcomp
            # with different options.
            _usepackage_if_not_loaded("textcomp"),
        ])
