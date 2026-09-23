    def writeInfoDict(self):
        """Write out the info dictionary, checking it for good form"""

        def is_string_like(x):
            return isinstance(x, str)

        def is_date(x):
            return isinstance(x, datetime)

        check_trapped = (lambda x: isinstance(x, Name) and
                         x.name in ('True', 'False', 'Unknown'))

        keywords = {'Title': is_string_like,
                    'Author': is_string_like,
                    'Subject': is_string_like,
                    'Keywords': is_string_like,
                    'Creator': is_string_like,
                    'Producer': is_string_like,
                    'CreationDate': is_date,
                    'ModDate': is_date,
                    'Trapped': check_trapped}
        for k in self.infoDict:
            if k not in keywords:
                warnings.warn('Unknown infodict keyword: %s' % k, stacklevel=2)
            else:
                if not keywords[k](self.infoDict[k]):
                    warnings.warn('Bad value for infodict keyword %s' % k,
                                  stacklevel=2)

        self.infoObject = self.reserveObject('info')
        self.writeObject(self.infoObject, self.infoDict)
