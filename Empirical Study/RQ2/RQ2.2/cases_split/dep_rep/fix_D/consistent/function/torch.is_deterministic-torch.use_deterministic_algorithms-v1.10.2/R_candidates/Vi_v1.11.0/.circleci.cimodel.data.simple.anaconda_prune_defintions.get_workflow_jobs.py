def get_workflow_jobs():
    return [gen_workflow_job(channel) for channel in CHANNELS_TO_PRUNE]
