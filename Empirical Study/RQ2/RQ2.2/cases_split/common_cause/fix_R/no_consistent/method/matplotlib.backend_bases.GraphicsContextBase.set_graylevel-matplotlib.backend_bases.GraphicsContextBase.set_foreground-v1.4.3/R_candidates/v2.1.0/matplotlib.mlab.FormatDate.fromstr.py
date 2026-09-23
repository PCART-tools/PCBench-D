    def fromstr(self, x):
        import dateutil.parser
        return dateutil.parser.parse(x).date()
