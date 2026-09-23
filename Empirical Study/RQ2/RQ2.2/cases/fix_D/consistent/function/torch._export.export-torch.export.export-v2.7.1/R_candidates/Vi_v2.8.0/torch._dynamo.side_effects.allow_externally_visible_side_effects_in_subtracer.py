@contextlib.contextmanager
def allow_externally_visible_side_effects_in_subtracer(tx: "InstructionTranslator"):
    orig_val = tx.output.current_tracer.unsafe_allow_externally_visible_side_effects
    try:
        tx.output.current_tracer.unsafe_allow_externally_visible_side_effects = True
        yield
    finally:
        tx.output.current_tracer.unsafe_allow_externally_visible_side_effects = orig_val
