def analyze(obj):
    """
    Given a Job, visits all the execution steps making sure that:
      - no undefined blobs will be found during execution
      - no blob with same name is defined in concurrent steps
    """
    Analyzer()(obj)
