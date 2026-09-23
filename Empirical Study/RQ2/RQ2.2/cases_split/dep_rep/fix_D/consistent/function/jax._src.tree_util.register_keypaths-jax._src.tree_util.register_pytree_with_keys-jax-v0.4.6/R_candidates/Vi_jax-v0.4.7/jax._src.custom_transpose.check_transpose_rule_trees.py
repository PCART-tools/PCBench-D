def check_transpose_rule_trees(rule, lin_tree, rule_out_tree):
  if not is_treedef_prefix(lin_tree, rule_out_tree):
    if hasattr(rule, '_transpose_type_error'):
      raise rule._transpose_type_error(lin_tree, rule_out_tree)
    else:
      raise TypeError(
          'structure of custom transpose rule\'s output does not prefix-match '
          'structure of primal function\'s linear inputs under '
          f'custom transpose rule ({rule_name(rule)}).\n'
          f'Transpose rule output: {rule_out_tree}\n'
          f'Linear primal inputs: {lin_tree}')
