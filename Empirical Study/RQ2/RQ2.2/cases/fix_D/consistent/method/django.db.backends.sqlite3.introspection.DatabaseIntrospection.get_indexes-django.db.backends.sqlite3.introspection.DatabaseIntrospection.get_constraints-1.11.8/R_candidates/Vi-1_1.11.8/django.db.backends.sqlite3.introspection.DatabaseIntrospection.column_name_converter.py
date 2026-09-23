    def column_name_converter(self, name):
        """
        SQLite will in some cases, e.g. when returning columns from views and
        subselects, return column names in 'alias."column"' format instead of
        simply 'column'.

        Affects SQLite < 3.7.15, fixed by http://www.sqlite.org/src/info/5526e0aa3c
        """
        # TODO: remove when SQLite < 3.7.15 is sufficiently old.
        # 3.7.13 ships in Debian stable as of 2014-03-21.
        if self.connection.Database.sqlite_version_info < (3, 7, 15):
            return name.split('.')[-1].strip('"')
        else:
            return name
