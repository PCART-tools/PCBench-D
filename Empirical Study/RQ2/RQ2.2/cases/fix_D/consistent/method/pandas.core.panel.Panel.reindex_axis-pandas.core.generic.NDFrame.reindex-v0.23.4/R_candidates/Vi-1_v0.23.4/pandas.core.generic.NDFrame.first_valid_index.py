    @Appender(_shared_docs['valid_index'] % {'position': 'first',
                                             'klass': 'NDFrame'})
    def first_valid_index(self):
        return self._find_valid_index('first')
