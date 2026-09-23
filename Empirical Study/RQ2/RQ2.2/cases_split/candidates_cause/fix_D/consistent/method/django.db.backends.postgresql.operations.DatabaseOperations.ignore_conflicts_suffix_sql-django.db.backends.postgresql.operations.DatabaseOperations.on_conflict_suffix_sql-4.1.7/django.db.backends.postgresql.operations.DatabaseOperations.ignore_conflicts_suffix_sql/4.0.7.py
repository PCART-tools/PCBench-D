    def ignore_conflicts_suffix_sql(self, ignore_conflicts=None):
        return (
            "ON CONFLICT DO NOTHING"
            if ignore_conflicts
            else super().ignore_conflicts_suffix_sql(ignore_conflicts)
        )
