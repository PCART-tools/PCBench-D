    def fetch_returned_insert_id(self, cursor):
        return int(cursor._insert_id_var.getvalue())
