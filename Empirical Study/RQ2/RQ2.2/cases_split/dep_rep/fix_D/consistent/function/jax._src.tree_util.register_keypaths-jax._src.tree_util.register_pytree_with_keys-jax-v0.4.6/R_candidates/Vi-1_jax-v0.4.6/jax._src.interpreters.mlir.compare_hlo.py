def compare_hlo(x, y, direction: str, comparison_type: Optional[str] = None):
  """Creates CompareOp."""
  if comparison_type is None:
    elem_type = ir.RankedTensorType(x.type).element_type
    if ir.IntegerType.isinstance(elem_type):
      comparison_type = ("UNSIGNED" if ir.IntegerType.is_unsigned(elem_type)
                         else "SIGNED")
    else:
      comparison_type = "FLOAT"

  return hlo.CompareOp(
      x,
      y,
      hlo.ComparisonDirectionAttr.get(direction),
      compare_type=hlo.ComparisonTypeAttr.get(comparison_type))
