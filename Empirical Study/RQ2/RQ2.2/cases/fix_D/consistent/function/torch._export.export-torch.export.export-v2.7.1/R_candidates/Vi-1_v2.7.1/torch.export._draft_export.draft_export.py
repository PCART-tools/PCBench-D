def draft_export(
    mod: torch.nn.Module,
    args: tuple[Any, ...],
    kwargs: Optional[dict[str, Any]] = None,
    *,
    dynamic_shapes: Optional[Union[dict[str, Any], tuple[Any], list[Any]]] = None,
    preserve_module_call_signature: tuple[str, ...] = (),
    strict: bool = False,
    pre_dispatch: bool = False,
) -> ExportedProgram:
    kwargs = kwargs or {}
    dynamic_shapes = dynamic_shapes or {}

    capture_structured_log = CaptureStructuredTrace()

    with torch._functorch.config.patch(
        fake_tensor_propagate_real_tensors=True,
        generate_fake_kernels_from_real_mismatches=True,
    ), capture_structured_log:
        try:
            new_shapes = None
            ep = _export(
                mod,
                args,
                kwargs,
                dynamic_shapes=dynamic_shapes,
                strict=strict,
                pre_dispatch=pre_dispatch,
                preserve_module_call_signature=preserve_module_call_signature,
            )
        except torch._dynamo.exc.UserError as exc:
            new_shapes = refine_dynamic_shapes_from_suggested_fixes(
                exc.msg, dynamic_shapes
            )
            ep = _export(
                mod,
                args,
                kwargs,
                dynamic_shapes=new_shapes,
                strict=strict,
                pre_dispatch=pre_dispatch,
                preserve_module_call_signature=preserve_module_call_signature,
            )

        torch._logging.dtrace_structured("exported_program", payload_fn=lambda: str(ep))

        str_to_filename: dict[int, str] = {}
        failures: list[FailureReport] = []
        custom_ops_logs: dict[
            Any, tuple[dict[str, Any], FailureType]
        ] = {}  # For adding in assertions before custom ops
        expressions_created: dict[int, dict[str, Any]] = {}

        for log_name, log_contents in capture_structured_log.log_record.logs:
            failure_type = None

            if log_name == "str":
                str_to_filename[log_contents[1]] = log_contents[0]  # type: ignore[index]
                continue

            elif log_name == "propagate_real_tensors_provenance":
                log_contents[
                    "occurrences"
                ] = capture_structured_log.log_record.get_log_count(
                    (log_name, log_contents)
                )

                failure_type = FailureType.DATA_DEPENDENT_ERROR

            elif log_name == "guard_added":
                if new_shapes is None:
                    continue

                failure_type = FailureType.CONSTRAINT_VIOLATION_ERROR
                if len(log_contents["symbol_to_sources"]) == 0:
                    # We only want to include guards added that are relevant to
                    # the symbolic shapes corresponding to the inputs which were
                    # specified in the dynamic_shapes arg. These have a source.
                    continue

                log_contents["new_dynamic_shapes"] = new_shapes
            elif log_name == "missing_fake_kernel":
                failure_type = FailureType.MISSING_FAKE_KERNEL
                custom_ops_logs[log_contents["op"]] = (log_contents, failure_type)

            elif log_name == "mismatched_fake_kernel":
                failure_type = FailureType.MISMATCHED_FAKE_KERNEL
                custom_ops_logs[(log_contents["op"], log_contents["reason"])] = (
                    log_contents,
                    failure_type,
                )

            else:
                continue

            assert failure_type is not None
            failures.append(
                FailureReport(
                    failure_type,
                    log_contents,
                )
            )

        for k, v in capture_structured_log.expression_created_logs.items():
            if v.visited:
                expressions_created[k] = v.record

        report = DraftExportReport(failures, str_to_filename, expressions_created)

        # Add asserts around custom ops
        insert_custom_op_guards(ep.graph_module, list(custom_ops_logs.keys()))

    ep._report = report
    if not report.successful():
        log_filename = capture_structured_log.stream.name

        log.warning(
            """
###################################################################################################
WARNING: %s issue(s) found during export, and it was not able to soundly produce a graph.
To view the report of failures in an html page, please run the command:
    `tlparse %s --export`
Or, you can view the errors in python by inspecting `print(ep._report)`.
###################################################################################################
        """,
            len(report.failures),
            log_filename,
        )
    else:
        log.info(
            """
##############################################################################################
Congratuations: No issues are found during export, and it was able to soundly produce a graph.
You can now change back to torch.export.export()
##############################################################################################
    """
        )

    return ep
