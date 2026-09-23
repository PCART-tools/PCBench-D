def merge_mlir_modules(dst_module: ir.Module,
                       sym_name: str,
                       src_module: ir.Module) -> str:
  """Returns the name of src_module's main() function, after renaming."""
  callee_name = None
  assert dst_module.context == src_module.context
  dst_symtab = ir.SymbolTable(dst_module.operation)

  n = len(dst_module.body.operations)
  for op in src_module.body.operations:
    dst_module.body.append(op)
  ops = list(dst_module.body.operations)[n:]

  for op in ops:
    op = typing.cast(func_dialect.FuncOp, op)
    old_name = op.name.value
    if op.name.value == "main":
      dst_symtab.set_symbol_name(op, sym_name)
      op.attributes["sym_visibility"] = ir.StringAttr.get("private")
      callee_name = ir.StringAttr(dst_symtab.insert(op)).value
      new_name = callee_name
    else:
      new_name = ir.StringAttr(dst_symtab.insert(op)).value

    # Replace references to the symbol with the new name
    for other_op in ops:
      dst_symtab.replace_all_symbol_uses(
          old_name, new_name, other_op.operation)


  assert callee_name is not None
  return callee_name
