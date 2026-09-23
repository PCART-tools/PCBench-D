    def delete_model(self, model):
        # Run superclass action
        super(DatabaseSchemaEditor, self).delete_model(model)
        # Clean up any autoincrement trigger
        self.execute("""
            DECLARE
                i INTEGER;
            BEGIN
                SELECT COUNT(1) INTO i FROM USER_SEQUENCES
                    WHERE SEQUENCE_NAME = '%(sq_name)s';
                IF i = 1 THEN
                    EXECUTE IMMEDIATE 'DROP SEQUENCE "%(sq_name)s"';
                END IF;
            END;
        /""" % {'sq_name': self.connection.ops._get_sequence_name(model._meta.db_table)})
