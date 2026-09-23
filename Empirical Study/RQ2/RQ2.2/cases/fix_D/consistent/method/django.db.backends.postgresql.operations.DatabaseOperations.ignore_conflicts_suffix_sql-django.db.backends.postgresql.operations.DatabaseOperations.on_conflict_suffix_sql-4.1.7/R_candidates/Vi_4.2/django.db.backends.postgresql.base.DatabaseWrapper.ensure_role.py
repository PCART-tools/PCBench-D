    def ensure_role(self):
        if self.connection is None:
            return False
        if new_role := self.settings_dict.get("OPTIONS", {}).get("assume_role"):
            with self.connection.cursor() as cursor:
                sql = self.ops.compose_sql("SET ROLE %s", [new_role])
                cursor.execute(sql)
            return True
        return False
