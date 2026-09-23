    def db_check(self, connection):
        """
        Return the database column check constraint for this field, for the
        provided connection. Works the same way as db_type() for the case that
        get_internal_type() does not map to a preexisting model field.
        """
        data = DictWrapper(self.__dict__, connection.ops.quote_name, "qn_")
        try:
            return connection.data_type_check_constraints[self.get_internal_type()] % data
        except KeyError:
            return None
