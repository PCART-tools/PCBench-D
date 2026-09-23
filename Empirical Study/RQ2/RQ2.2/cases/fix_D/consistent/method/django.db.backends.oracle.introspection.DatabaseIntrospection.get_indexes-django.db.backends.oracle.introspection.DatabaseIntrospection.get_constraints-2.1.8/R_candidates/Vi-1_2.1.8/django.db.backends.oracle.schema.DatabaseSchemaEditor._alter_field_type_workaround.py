    def _alter_field_type_workaround(self, model, old_field, new_field):
        """
        Oracle refuses to change from some type to other type.
        What we need to do instead is:
        - Add a nullable version of the desired field with a temporary name. If
          the new column is an auto field, then the temporary column can't be
          nullable.
        - Update the table to transfer values from old to new
        - Drop old column
        - Rename the new column and possibly drop the nullable property
        """
        # Make a new field that's like the new one but with a temporary
        # column name.
        new_temp_field = copy.deepcopy(new_field)
        new_temp_field.null = (new_field.get_internal_type() not in ('AutoField', 'BigAutoField'))
        new_temp_field.column = self._generate_temp_name(new_field.column)
        # Add it
        self.add_field(model, new_temp_field)
        # Explicit data type conversion
        # https://docs.oracle.com/database/121/SQLRF/sql_elements002.htm#SQLRF51054
        new_value = self.quote_name(old_field.column)
        old_type = old_field.db_type(self.connection)
        if re.match('^N?CLOB', old_type):
            new_value = "TO_CHAR(%s)" % new_value
            old_type = 'VARCHAR2'
        if re.match('^N?VARCHAR2', old_type):
            new_internal_type = new_field.get_internal_type()
            if new_internal_type == 'DateField':
                new_value = "TO_DATE(%s, 'YYYY-MM-DD')" % new_value
            elif new_internal_type == 'DateTimeField':
                new_value = "TO_TIMESTAMP(%s, 'YYYY-MM-DD HH24:MI:SS.FF')" % new_value
            elif new_internal_type == 'TimeField':
                # TimeField are stored as TIMESTAMP with a 1900-01-01 date part.
                new_value = "TO_TIMESTAMP(CONCAT('1900-01-01 ', %s), 'YYYY-MM-DD HH24:MI:SS.FF')" % new_value
        # Transfer values across
        self.execute("UPDATE %s set %s=%s" % (
            self.quote_name(model._meta.db_table),
            self.quote_name(new_temp_field.column),
            new_value,
        ))
        # Drop the old field
        self.remove_field(model, old_field)
        # Rename and possibly make the new field NOT NULL
        super().alter_field(model, new_temp_field, new_field)
