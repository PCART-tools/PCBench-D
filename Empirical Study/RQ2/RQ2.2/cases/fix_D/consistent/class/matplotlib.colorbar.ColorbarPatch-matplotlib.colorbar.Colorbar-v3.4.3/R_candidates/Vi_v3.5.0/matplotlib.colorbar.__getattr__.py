@_api.caching_module_getattr  # module-level deprecations
class __getattr__:
    colorbar_doc = _api.deprecated("3.4", obj_type="")(property(
        lambda self: docstring.interpd.params["colorbar_doc"]))
    colorbar_kw_doc = _api.deprecated("3.4", obj_type="")(property(
        lambda self: _colormap_kw_doc))
    make_axes_kw_doc = _api.deprecated("3.4", obj_type="")(property(
        lambda self: _make_axes_param_doc + _make_axes_other_param_doc))
