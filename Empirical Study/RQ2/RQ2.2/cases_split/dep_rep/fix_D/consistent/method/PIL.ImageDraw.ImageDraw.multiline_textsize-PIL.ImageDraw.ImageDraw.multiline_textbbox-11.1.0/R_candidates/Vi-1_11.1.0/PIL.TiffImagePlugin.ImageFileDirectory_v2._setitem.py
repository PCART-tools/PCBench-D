    def _setitem(self, tag: int, value: Any, legacy_api: bool) -> None:
        basetypes = (Number, bytes, str)

        info = TiffTags.lookup(tag, self.group)
        values = [value] if isinstance(value, basetypes) else value

        if tag not in self.tagtype:
            if info.type:
                self.tagtype[tag] = info.type
            else:
                self.tagtype[tag] = TiffTags.UNDEFINED
                if all(isinstance(v, IFDRational) for v in values):
                    for v in values:
                        assert isinstance(v, IFDRational)
                        if v < 0:
                            self.tagtype[tag] = TiffTags.SIGNED_RATIONAL
                            break
                    else:
                        self.tagtype[tag] = TiffTags.RATIONAL
                elif all(isinstance(v, int) for v in values):
                    short = True
                    signed_short = True
                    long = True
                    for v in values:
                        assert isinstance(v, int)
                        if short and not (0 <= v < 2**16):
                            short = False
                        if signed_short and not (-(2**15) < v < 2**15):
                            signed_short = False
                        if long and v < 0:
                            long = False
                    if short:
                        self.tagtype[tag] = TiffTags.SHORT
                    elif signed_short:
                        self.tagtype[tag] = TiffTags.SIGNED_SHORT
                    elif long:
                        self.tagtype[tag] = TiffTags.LONG
                    else:
                        self.tagtype[tag] = TiffTags.SIGNED_LONG
                elif all(isinstance(v, float) for v in values):
                    self.tagtype[tag] = TiffTags.DOUBLE
                elif all(isinstance(v, str) for v in values):
                    self.tagtype[tag] = TiffTags.ASCII
                elif all(isinstance(v, bytes) for v in values):
                    self.tagtype[tag] = TiffTags.BYTE

        if self.tagtype[tag] == TiffTags.UNDEFINED:
            values = [
                v.encode("ascii", "replace") if isinstance(v, str) else v
                for v in values
            ]
        elif self.tagtype[tag] == TiffTags.RATIONAL:
            values = [float(v) if isinstance(v, int) else v for v in values]

        is_ifd = self.tagtype[tag] == TiffTags.LONG and isinstance(values, dict)
        if not is_ifd:
            values = tuple(
                info.cvt_enum(value) if isinstance(value, str) else value
                for value in values
            )

        dest = self._tags_v1 if legacy_api else self._tags_v2

        # Three branches:
        # Spec'd length == 1, Actual length 1, store as element
        # Spec'd length == 1, Actual > 1, Warn and truncate. Formerly barfed.
        # No Spec, Actual length 1, Formerly (<4.2) returned a 1 element tuple.
        # Don't mess with the legacy api, since it's frozen.
        if not is_ifd and (
            (info.length == 1)
            or self.tagtype[tag] == TiffTags.BYTE
            or (info.length is None and len(values) == 1 and not legacy_api)
        ):
            # Don't mess with the legacy api, since it's frozen.
            if legacy_api and self.tagtype[tag] in [
                TiffTags.RATIONAL,
                TiffTags.SIGNED_RATIONAL,
            ]:  # rationals
                values = (values,)
            try:
                (dest[tag],) = values
            except ValueError:
                # We've got a builtin tag with 1 expected entry
                warnings.warn(
                    f"Metadata Warning, tag {tag} had too many entries: "
                    f"{len(values)}, expected 1"
                )
                dest[tag] = values[0]

        else:
            # Spec'd length > 1 or undefined
            # Unspec'd, and length > 1
            dest[tag] = values
