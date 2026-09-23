def raise_unhashable(arg, tx=None):
    if tx is None:
        from torch._dynamo.symbolic_convert import InstructionTranslator

        tx = InstructionTranslator.current_tx()
    raise_observed_exception(
        TypeError, tx, args=[ConstantVariable(f"unhashable type: {type(arg)}")]
    )
