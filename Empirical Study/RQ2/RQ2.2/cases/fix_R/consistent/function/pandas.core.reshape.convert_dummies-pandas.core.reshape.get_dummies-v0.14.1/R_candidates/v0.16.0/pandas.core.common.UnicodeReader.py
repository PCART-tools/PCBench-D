    def UnicodeReader(f, dialect=csv.excel, encoding="utf-8", **kwds):
        # ignore encoding
        return csv.reader(f, dialect=dialect, **kwds)
