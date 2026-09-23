    def UnicodeWriter(f, dialect=csv.excel, encoding="utf-8", **kwds):
        return csv.writer(f, dialect=dialect, **kwds)
