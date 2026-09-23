    def _find_fonts_by_props(self, prop, fontext='ttf', directory=None,
                             fallback_to_default=True, rebuild_if_missing=True):
        """
        Find the paths to the font files most closely matching the given properties.

        Parameters
        ----------
        prop : str or `~matplotlib.font_manager.FontProperties`
            The font properties to search for. This can be either a
            `.FontProperties` object or a string defining a
            `fontconfig patterns`_.

        fontext : {'ttf', 'afm'}, default: 'ttf'
            The extension of the font file:

            - 'ttf': TrueType and OpenType fonts (.ttf, .ttc, .otf)
            - 'afm': Adobe Font Metrics (.afm)

        directory : str, optional
            If given, only search this directory and its subdirectories.

        fallback_to_default : bool
            If True, will fall back to the default font family (usually
            "DejaVu Sans" or "Helvetica") if none of the families were found.

        rebuild_if_missing : bool
            Whether to rebuild the font cache and search again if the first
            match appears to point to a nonexisting font (i.e., the font cache
            contains outdated entries).

        Returns
        -------
        list[str]
            The paths of the fonts found.

        Notes
        -----
        This is an extension/wrapper of the original findfont API, which only
        returns a single font for given font properties. Instead, this API
        returns a list of filepaths of multiple fonts which closely match the
        given font properties.  Since this internally uses the original API,
        there's no change to the logic of performing the nearest neighbor
        search.  See `findfont` for more details.
        """

        prop = FontProperties._from_any(prop)

        fpaths = []
        for family in prop.get_family():
            cprop = prop.copy()
            cprop.set_family(family)  # set current prop's family

            try:
                fpaths.append(
                    self.findfont(
                        cprop, fontext, directory,
                        fallback_to_default=False,  # don't fallback to default
                        rebuild_if_missing=rebuild_if_missing,
                    )
                )
            except ValueError:
                if family in font_family_aliases:
                    _log.warning(
                        "findfont: Generic family %r not found because "
                        "none of the following families were found: %s",
                        family, ", ".join(self._expand_aliases(family))
                    )
                else:
                    _log.warning("findfont: Font family %r not found.", family)

        # only add default family if no other font was found and
        # fallback_to_default is enabled
        if not fpaths:
            if fallback_to_default:
                dfamily = self.defaultFamily[fontext]
                cprop = prop.copy()
                cprop.set_family(dfamily)
                fpaths.append(
                    self.findfont(
                        cprop, fontext, directory,
                        fallback_to_default=True,
                        rebuild_if_missing=rebuild_if_missing,
                    )
                )
            else:
                raise ValueError("Failed to find any font, and fallback "
                                 "to the default font was disabled")

        return fpaths
