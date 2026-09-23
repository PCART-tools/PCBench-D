def _if_refresh_overridden_call_and_emit_deprec(locator):
    if not locator.refresh.__func__.__module__.startswith("matplotlib."):
        cbook.warn_external(
            "3.3", message="Automatic calls to Locator.refresh by the draw "
            "machinery are deprecated since %(since)s and will be removed in "
            "%(removal)s.  You are using a third-party locator that overrides "
            "the refresh() method; this locator should instead perform any "
            "required processing in __call__().")
    with _api.suppress_matplotlib_deprecation_warning():
        locator.refresh()
