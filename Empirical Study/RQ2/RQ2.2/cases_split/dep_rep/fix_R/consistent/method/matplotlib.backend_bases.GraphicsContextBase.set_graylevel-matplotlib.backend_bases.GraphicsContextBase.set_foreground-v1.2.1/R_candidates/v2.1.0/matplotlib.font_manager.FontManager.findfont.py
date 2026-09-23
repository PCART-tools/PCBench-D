    def findfont(self, prop, fontext='ttf', directory=None,
                 fallback_to_default=True, rebuild_if_missing=True):
        """
        Search the font list for the font that most closely matches
        the :class:`FontProperties` *prop*.

        :meth:`findfont` performs a nearest neighbor search.  Each
        font is given a similarity score to the target font
        properties.  The first font with the highest score is
        returned.  If no matches below a certain threshold are found,
        the default font (usually DejaVu Sans) is returned.

        `directory`, is specified, will only return fonts from the
        given directory (or subdirectory of that directory).

        The result is cached, so subsequent lookups don't have to
        perform the O(n) nearest neighbor search.

        If `fallback_to_default` is True, will fallback to the default
        font family (usually "DejaVu Sans" or "Helvetica") if
        the first lookup hard-fails.

        See the `W3C Cascading Style Sheet, Level 1
        <http://www.w3.org/TR/1998/REC-CSS2-19980512/>`_ documentation
        for a description of the font finding algorithm.
        """
        if not isinstance(prop, FontProperties):
            prop = FontProperties(prop)
        fname = prop.get_file()
        if fname is not None:
            verbose.report('findfont returning %s'%fname, 'debug')
            return fname

        if fontext == 'afm':
            fontlist = self.afmlist
        else:
            fontlist = self.ttflist

        if directory is None:
            cached = _lookup_cache[fontext].get(prop)
            if cached is not None:
                return cached
        else:
            directory = os.path.normcase(directory)

        best_score = 1e64
        best_font = None

        for font in fontlist:
            if (directory is not None and
                    os.path.commonprefix([os.path.normcase(font.fname),
                                          directory]) != directory):
                continue
            # Matching family should have highest priority, so it is multiplied
            # by 10.0
            score = \
                self.score_family(prop.get_family(), font.name) * 10.0 + \
                self.score_style(prop.get_style(), font.style) + \
                self.score_variant(prop.get_variant(), font.variant) + \
                self.score_weight(prop.get_weight(), font.weight) + \
                self.score_stretch(prop.get_stretch(), font.stretch) + \
                self.score_size(prop.get_size(), font.size)
            if score < best_score:
                best_score = score
                best_font = font
            if score == 0:
                break

        if best_font is None or best_score >= 10.0:
            if fallback_to_default:
                warnings.warn(
                    'findfont: Font family %s not found. Falling back to %s' %
                    (prop.get_family(), self.defaultFamily[fontext]))
                default_prop = prop.copy()
                default_prop.set_family(self.defaultFamily[fontext])
                return self.findfont(default_prop, fontext, directory, False)
            else:
                # This is a hard fail -- we can't find anything reasonable,
                # so just return the DejuVuSans.ttf
                warnings.warn(
                    'findfont: Could not match %s. Returning %s' %
                    (prop, self.defaultFont[fontext]),
                    UserWarning)
                result = self.defaultFont[fontext]
        else:
            verbose.report(
                'findfont: Matching %s to %s (%s) with score of %f' %
                (prop, best_font.name, repr(best_font.fname), best_score))
            result = best_font.fname

        if not os.path.isfile(result):
            if rebuild_if_missing:
                verbose.report(
                    'findfont: Found a missing font file.  Rebuilding cache.')
                _rebuild()
                return fontManager.findfont(
                    prop, fontext, directory, True, False)
            else:
                raise ValueError("No valid font could be found")

        if directory is None:
            _lookup_cache[fontext].set(prop, result)
        return result
