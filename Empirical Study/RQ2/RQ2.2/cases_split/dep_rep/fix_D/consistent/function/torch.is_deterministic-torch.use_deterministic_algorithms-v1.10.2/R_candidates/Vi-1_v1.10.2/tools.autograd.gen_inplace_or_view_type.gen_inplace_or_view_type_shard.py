def gen_inplace_or_view_type_shard(
    fm: FileManager, fns_with_infos: List[NativeFunctionWithDifferentiabilityInfo], suffix: str
) -> None:

    filtered_fns_with_infos = list(filter(use_derived, fns_with_infos))

    fm.write_with_template('ADInplaceOrViewType%s.cpp' % suffix, 'ADInplaceOrViewType.cpp', lambda: {
        'generated_comment': f'@generated from {fm.template_dir}/ADInplaceOrViewType.cpp',
        'inplace_or_view_method_definitions': list(mapMaybe(inplace_or_view_method_definition, filtered_fns_with_infos)),
        'inplace_or_view_wrapper_registrations': list(mapMaybe(inplace_or_view_method_registration, filtered_fns_with_infos)),
    })
