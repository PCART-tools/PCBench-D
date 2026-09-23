def guard_collectives_hook(guard_eval_result):
    import torch.distributed as dist
    from torch._dynamo.utils import dynamo_timed

    # guard_eval_result == True  ==>  cache hit
    if pg := distributed.get_guard_pg():
        with dynamo_timed(
            "guard_collective", log_pt2_compile_event=True, log_waitcounter=True
        ):
            log.info("guard_collective %s", guard_eval_result)
            torch._logging.trace_structured(
                "artifact",
                metadata_fn=lambda: {
                    "name": "guard_collective",
                    "encoding": "string",
                },
                payload_fn=lambda: str(guard_eval_result),
            )
            # TODO: a bit awkward to time, this isn't inside of the dynamo compile region
            all_results = [None] * pg.size()
            dist.all_gather_object(all_results, guard_eval_result, group=pg)
            # True = everyone hit, OK to run
            # False = someone missed, force recompile everywhere
            res = all(all_results)
            log.info("guard_collective %s -> %s", guard_eval_result, res)
            return res
    return guard_eval_result
