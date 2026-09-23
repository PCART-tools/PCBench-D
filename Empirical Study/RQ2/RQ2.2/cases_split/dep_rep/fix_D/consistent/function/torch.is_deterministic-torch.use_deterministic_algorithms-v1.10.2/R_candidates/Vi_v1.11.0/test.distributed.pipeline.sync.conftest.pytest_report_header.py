def pytest_report_header():
    return f"torch: {torch.__version__}"
