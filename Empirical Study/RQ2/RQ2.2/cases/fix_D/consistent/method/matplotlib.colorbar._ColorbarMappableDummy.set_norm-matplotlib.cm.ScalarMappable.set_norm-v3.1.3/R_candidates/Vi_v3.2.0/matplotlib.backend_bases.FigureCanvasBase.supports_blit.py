    @cbook._classproperty
    def supports_blit(cls):
        return (hasattr(cls, "copy_from_bbox")
                and hasattr(cls, "restore_region"))
