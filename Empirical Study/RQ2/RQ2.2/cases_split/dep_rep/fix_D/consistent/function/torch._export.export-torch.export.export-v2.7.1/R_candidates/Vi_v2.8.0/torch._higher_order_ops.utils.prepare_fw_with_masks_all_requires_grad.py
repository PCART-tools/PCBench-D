def prepare_fw_with_masks_all_requires_grad(fn):
    def fw_with_masks(*args):
        fw_out = fn(*args)
        # Note [force all outputs to be require grad]
        # Instead of using the original fn, we set the output of original
        # fn to all require grad. This is consistent with the behavior
        # of autograd.Function, where if any one of the inputs requires grad
        # all output will be require grad. This also makes the downstream
        # require_gradness reasoning much easier.
        if pytree.tree_any_only(torch.Tensor, lambda t: t.requires_grad, args):
            fw_out = pytree.tree_map_only(
                torch.Tensor, lambda x: x.requires_grad_(True), fw_out
            )
        return fw_out, pytree.tree_map_only(
            torch.Tensor, lambda x: x.requires_grad, fw_out
        )

    return fw_with_masks
