    @event_hooks.setter
    def event_hooks(
        self, event_hooks: typing.Dict[str, typing.List[typing.Callable]]
    ) -> None:
        self._event_hooks = {
            "request": list(event_hooks.get("request", [])),
            "response": list(event_hooks.get("response", [])),
        }
