def check_meta_consistency(
    lhs_list: list[Union[torch.Tensor, torch.SymInt, int]],
    rhs_list: list[Union[torch.Tensor, torch.SymInt, int]],
    lhs_name: str,
    rhs_name: str,
) -> None:
    def diff_meta_pairs(
        lhs_list: list[Union[torch.Tensor, torch.SymInt, int]],
        rhs_list: list[Union[torch.Tensor, torch.SymInt, int]],
    ) -> list[str]:
        def diff_meta(
            lhs: Union[torch.Tensor, torch.SymInt, int],
            rhs: Union[torch.Tensor, torch.SymInt, int],
        ) -> str:
            if isinstance(lhs, torch.Tensor) and isinstance(rhs, torch.Tensor):
                return ", ".join(
                    diff_tensor_meta(
                        # We set include contiguity=False because we have vmap x cond tests, where if
                        # include_contiguity=True will call t.is_contiguous inside of vmap and get an error
                        # "querying is_contiguous inside of vmap for memory_format other than
                        # torch.contiguous_format is not yet implemented". This is good for because stride
                        # is still checked.
                        _extract_tensor_metadata(lhs, include_contiguity=False),
                        _extract_tensor_metadata(rhs, include_contiguity=False),
                        check_grad=False,
                    )
                )
            else:

                def _both_int_types(lhs, rhs):
                    return isinstance(lhs, (int, torch.SymInt)) and isinstance(
                        rhs, (int, torch.SymInt)
                    )

                def _both_tensor(lhs, rhs):
                    return isinstance(lhs, torch.Tensor) and isinstance(
                        rhs, torch.Tensor
                    )

                if not _both_int_types(lhs, rhs) and not _both_tensor(lhs, rhs):
                    return f"type: {lhs} vs {rhs}"

            return ""

        # Manually check the device of lhs and rhs as this field is currently not part of TensorMetadata
        def diff_device(
            lhs: Union[torch.Tensor, torch.SymInt, int],
            rhs: Union[torch.Tensor, torch.SymInt, int],
        ) -> str:
            if isinstance(lhs, torch.Tensor) and isinstance(rhs, torch.Tensor):
                if (
                    rhs.device.type == lhs.device.type
                    and rhs.device.index == lhs.device.index
                ):
                    return ""
                else:
                    return "device"
            return ""

        if len(lhs_list) != len(rhs_list):
            raise torch._dynamo.exc.UncapturedHigherOrderOpError(
                f"Expected {lhs_name} and {rhs_name} to have same number of outputs but got lhs:{lhs_list} and rhs:{rhs_list}"
            )
        all_diffs = []
        for i, (lhs, rhs) in enumerate(zip(lhs_list, rhs_list)):
            if diff := diff_meta(lhs, rhs):
                all_diffs.append(
                    f"pair[{i}] differ in {diff}, where lhs is {lhs} and rhs is {rhs}"
                )
            if diff := diff_device(lhs, rhs):
                all_diffs.append(
                    f"pair[{i}] differ in {diff}, where lhs is {lhs} and rhs is {rhs}"
                )
        return all_diffs

    if all_diffs := diff_meta_pairs(lhs_list, rhs_list):
        diff_str = "\n".join(all_diffs)
        raise torch._dynamo.exc.UncapturedHigherOrderOpError(
            f"Expected {lhs_name} and {rhs_name} to have same metadata but found:\n{diff_str}"
        )
