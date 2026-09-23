    def cache_key_culling_sql(self):
        return 'SELECT cache_key FROM %s ORDER BY cache_key OFFSET %%s ROWS FETCH FIRST 1 ROWS ONLY'
