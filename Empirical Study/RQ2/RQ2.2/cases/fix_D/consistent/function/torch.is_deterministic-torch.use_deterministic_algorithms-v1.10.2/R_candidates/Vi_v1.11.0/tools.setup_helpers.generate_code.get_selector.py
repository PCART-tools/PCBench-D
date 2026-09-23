def get_selector(
    selected_op_list_path: Optional[str],
    operators_yaml_path: Optional[str],
) -> Any:
    # cwrap depends on pyyaml, so we can't import it earlier
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, root)
    from tools.codegen.selective_build.selector import SelectiveBuilder

    assert not (selected_op_list_path is not None and
                operators_yaml_path is not None), \
        ("Expected at most one of selected_op_list_path and " +
         "operators_yaml_path to be set.")

    if selected_op_list_path is None and operators_yaml_path is None:
        return SelectiveBuilder.get_nop_selector()
    elif selected_op_list_path is not None:
        return get_selector_from_legacy_operator_selection_list(selected_op_list_path)
    else:
        return SelectiveBuilder.from_yaml_path(cast(str, operators_yaml_path))
