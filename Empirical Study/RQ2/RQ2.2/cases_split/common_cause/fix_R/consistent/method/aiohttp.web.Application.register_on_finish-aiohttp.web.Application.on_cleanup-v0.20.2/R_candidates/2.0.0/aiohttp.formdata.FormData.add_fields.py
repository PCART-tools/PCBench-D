    def add_fields(self, *fields):
        to_add = list(fields)

        while to_add:
            rec = to_add.pop(0)

            if isinstance(rec, io.IOBase):
                k = guess_filename(rec, 'unknown')
                self.add_field(k, rec)

            elif isinstance(rec, (MultiDictProxy, MultiDict)):
                to_add.extend(rec.items())

            elif isinstance(rec, (list, tuple)) and len(rec) == 2:
                k, fp = rec
                self.add_field(k, fp)

            else:
                raise TypeError('Only io.IOBase, multidict and (name, file) '
                                'pairs allowed, use .add_field() for passing '
                                'more complex parameters, got {!r}'
                                .format(rec))
