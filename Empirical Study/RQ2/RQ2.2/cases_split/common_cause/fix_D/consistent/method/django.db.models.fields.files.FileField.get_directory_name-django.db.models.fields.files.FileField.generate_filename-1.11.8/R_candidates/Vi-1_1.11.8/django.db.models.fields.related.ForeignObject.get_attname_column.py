    def get_attname_column(self):
        attname, column = super(ForeignObject, self).get_attname_column()
        return attname, None
