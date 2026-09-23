    def _commit(self):
        if self.connection is not None:
            try:
                return self.connection.commit()
            except Database.DatabaseError as e:
                # cx_Oracle raises a cx_Oracle.DatabaseError exception
                # with the following attributes and values:
                #  code = 2091
                #  message = 'ORA-02091: transaction rolled back
                #            'ORA-02291: integrity constraint (TEST_DJANGOTEST.SYS
                #               _C00102056) violated - parent key not found'
                # We convert that particular case to our IntegrityError exception
                x = e.args[0]
                if hasattr(x, 'code') and hasattr(x, 'message') \
                   and x.code == 2091 and 'ORA-02291' in x.message:
                    six.reraise(utils.IntegrityError, utils.IntegrityError(*tuple(e.args)), sys.exc_info()[2])
                raise
