    def enable_constraint_checking(self):
        self.cursor().execute('PRAGMA foreign_keys = ON')
