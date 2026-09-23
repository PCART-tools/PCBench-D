def gen_job_name(phase):
    job_name_parts = [
        "pytorch",
        "bazel",
        phase,
    ]

    return "_".join(job_name_parts)
