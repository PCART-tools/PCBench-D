    def get_queryset(self, **hints):
        return self.related.related_model._base_manager.db_manager(hints=hints).all()
