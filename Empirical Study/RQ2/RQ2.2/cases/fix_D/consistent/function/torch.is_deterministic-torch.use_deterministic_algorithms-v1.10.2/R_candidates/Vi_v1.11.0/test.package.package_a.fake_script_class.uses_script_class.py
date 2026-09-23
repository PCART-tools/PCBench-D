@torch.jit.script
def uses_script_class(x):
    """Intended to be scripted."""
    foo = MyScriptClass(x)
    return foo.foo
