def _find_arg_mismatch(arg_list, fails, fun_name):
  first_err, second_err = fails
  mismatched_args_msg = []
  for name, inp_da, aval in arg_list:
    if first_err.m_type == pxla.MismatchType.ARG_SHARDING:
      if first_err.da == inp_da:
        mismatched_args_msg.append(
            f"argument {name} of {fun_name} with shape {aval.str_short()} and "
             f"{first_err._dev_ids_plat_str}")
        break

  for name, inp_da, aval in arg_list:
    if second_err.m_type == pxla.MismatchType.ARG_SHARDING:
      if second_err.da == inp_da:
        mismatched_args_msg.append(
            f"argument {name} of {fun_name} with shape {aval.str_short()} and "
             f"{second_err._dev_ids_plat_str}")
        break
  return mismatched_args_msg
