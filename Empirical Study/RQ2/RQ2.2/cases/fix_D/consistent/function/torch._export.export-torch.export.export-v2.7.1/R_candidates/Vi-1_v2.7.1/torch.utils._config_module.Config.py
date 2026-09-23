    def Config(
        default: Union[T, object] = _UNSET_SENTINEL,
        justknob: Optional[str] = None,
        env_name_default: Optional[Union[str, list[str]]] = None,
        env_name_force: Optional[Union[str, list[str]]] = None,
        value_type: Optional[type] = None,
        alias: Optional[str] = None,
    ) -> _Config[T]:
        return _Config(
            default, justknob, env_name_default, env_name_force, value_type, alias
        )
