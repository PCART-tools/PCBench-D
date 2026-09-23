def _must_dispatch_in_python(args, kwargs):
    return pytree.tree_any(
        lambda obj: isinstance(
            obj, torch._library.fake_class_registry.FakeScriptObject
        ),
        (args, kwargs),
    )
