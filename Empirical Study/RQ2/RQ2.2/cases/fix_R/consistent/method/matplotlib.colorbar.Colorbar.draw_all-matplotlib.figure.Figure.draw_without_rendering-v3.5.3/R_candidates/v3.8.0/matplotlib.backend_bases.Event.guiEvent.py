    @property
    def guiEvent(self):
        # After deprecation elapses: remove _guiEvent_deleted; make guiEvent a plain
        # attribute set to None by _process.
        if self._guiEvent_deleted:
            _api.warn_deprecated(
                "3.8", message="Accessing guiEvent outside of the original GUI event "
                "handler is unsafe and deprecated since %(since)s; in the future, the "
                "attribute will be set to None after quitting the event handler.  You "
                "may separately record the value of the guiEvent attribute at your own "
                "risk.")
        return self._guiEvent
