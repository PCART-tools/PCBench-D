@_api.caching_module_getattr
class __getattr__:
    locals().update({
        name: _api.deprecated("3.4")(
            property(lambda self, _mod=mod, _name=name: getattr(_mod, _name)))
        for mod, names in [
            (_mathtext, ["SHRINK_FACTOR", "GROW_FACTOR", "NUM_SIZE_LEVELS"]),
            (_mathtext_data, [
                "latex_to_bakoma", "latex_to_cmex", "latex_to_standard",
                "stix_virtual_fonts", "tex2uni"])]
        for name in names})
