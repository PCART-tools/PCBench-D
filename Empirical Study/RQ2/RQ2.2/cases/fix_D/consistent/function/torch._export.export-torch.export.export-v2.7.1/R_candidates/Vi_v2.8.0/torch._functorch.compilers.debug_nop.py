@make_boxed_compiler
def debug_nop(fx_g: fx.GraphModule, _) -> Callable:
    """
    Returns a (slow) interpreter over the FX graph module that also checks
    various debugging properties (e.g., that tracing strides matched real
    strides.)
    """
    return DebugInterpreter(fx_g).run
