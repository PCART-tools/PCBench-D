    def __getitem__(self, texname):
        assert isinstance(texname, bytes)
        if texname in self._unparsed:
            for line in self._unparsed.pop(texname):
                if self._parse_and_cache_line(line):
                    break
        try:
            return self._parsed[texname]
        except KeyError:
            raise LookupError(
                f"An associated PostScript font (required by Matplotlib) "
                f"could not be found for TeX font {texname.decode('ascii')!r} "
                f"in {self._filename!r}; this problem can often be solved by "
                f"installing a suitable PostScript font package in your TeX "
                f"package manager") from None
