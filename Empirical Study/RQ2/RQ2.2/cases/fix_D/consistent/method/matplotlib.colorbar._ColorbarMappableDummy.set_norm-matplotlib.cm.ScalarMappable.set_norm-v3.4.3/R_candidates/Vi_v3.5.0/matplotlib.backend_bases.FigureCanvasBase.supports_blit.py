    @_api.classproperty
    def supports_blit(cls):
        """If this Canvas sub-class supports blitting."""
        return (hasattr(cls, "copy_from_bbox")
                and hasattr(cls, "restore_region"))
