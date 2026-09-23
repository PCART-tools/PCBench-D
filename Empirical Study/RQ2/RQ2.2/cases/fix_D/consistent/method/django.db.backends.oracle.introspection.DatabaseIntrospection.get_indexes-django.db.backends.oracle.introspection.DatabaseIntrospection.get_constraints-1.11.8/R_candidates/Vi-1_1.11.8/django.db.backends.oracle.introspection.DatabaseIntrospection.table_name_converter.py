    def table_name_converter(self, name):
        "Table name comparison is case insensitive under Oracle"
        return name.lower()
