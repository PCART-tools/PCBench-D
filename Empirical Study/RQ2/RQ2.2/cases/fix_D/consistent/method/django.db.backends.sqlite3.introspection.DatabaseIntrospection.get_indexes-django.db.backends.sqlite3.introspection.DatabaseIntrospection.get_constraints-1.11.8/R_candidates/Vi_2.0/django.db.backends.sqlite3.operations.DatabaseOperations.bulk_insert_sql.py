    def bulk_insert_sql(self, fields, placeholder_rows):
        return " UNION ALL ".join(
            "SELECT %s" % ", ".join(row)
            for row in placeholder_rows
        )
