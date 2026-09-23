def example_job():
    with Job() as job:
        with job.init_group:
            example_loop()
        example_task()
    return job
