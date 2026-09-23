    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        """
        Return a list of SQL statements required to remove all data from
        the given database tables (without actually removing the tables
        themselves) and the SQL statements required to reset the sequences
        passed in `sequences`.

        The `style` argument is a Style object as returned by either
        color_style() or no_style() in django.core.management.color.

        The `allow_cascade` argument determines whether truncation may cascade
        to tables with foreign keys pointing the tables being truncated.
        PostgreSQL requires a cascade even if these tables are empty.
        """
        raise NotImplementedError('subclasses of BaseDatabaseOperations must provide an sql_flush() method')
