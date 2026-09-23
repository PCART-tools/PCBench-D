def main() -> None:
    jinja_env = jinja2.Environment(
        variable_start_string="!{{",
        loader=jinja2.FileSystemLoader(str(GITHUB_DIR.joinpath("templates"))),
        undefined=jinja2.StrictUndefined,
    )
    template_and_workflows = [
        (jinja_env.get_template("linux_ci_workflow.yml.j2"), LINUX_WORKFLOWS),
        (jinja_env.get_template("linux_ci_workflow.yml.j2"), XLA_WORKFLOWS),
        (jinja_env.get_template("windows_ci_workflow.yml.j2"), WINDOWS_WORKFLOWS),
        (jinja_env.get_template("bazel_ci_workflow.yml.j2"), BAZEL_WORKFLOWS),
        (jinja_env.get_template("ios_ci_workflow.yml.j2"), IOS_WORKFLOWS),
        (jinja_env.get_template("macos_ci_workflow.yml.j2"), MACOS_WORKFLOWS),
        (jinja_env.get_template("docker_builds_ci_workflow.yml.j2"), DOCKER_WORKFLOWS),
        (jinja_env.get_template("android_ci_full_workflow.yml.j2"), ANDROID_WORKFLOWS),
        (jinja_env.get_template("android_ci_workflow.yml.j2"), ANDROID_SHORT_WORKFLOWS),
        (jinja_env.get_template("linux_binary_build_workflow.yml.j2"), LINUX_BINARY_BUILD_WORFKLOWS),
        (jinja_env.get_template("windows_binary_build_workflow.yml.j2"), WINDOWS_BINARY_BUILD_WORKFLOWS),
    ]
    # Delete the existing generated files first, this should align with .gitattributes file description.
    existing_workflows = GITHUB_DIR.glob("workflows/generated-*")
    for w in existing_workflows:
        try:
            os.remove(w)
        except Exception as e:
            print(f"Error occurred when deleting file {w}: {e}")

    ciflow_ruleset = CIFlowRuleset()
    for template, workflows in template_and_workflows:
        # added Iterable check to appease the mypy gods
        if not isinstance(workflows, Iterable):
            raise Exception(f"How is workflows not iterable? {workflows}")
        for workflow in workflows:
            workflow.generate_workflow_file(workflow_template=template)
            ciflow_ruleset.add_label_rule(workflow.ciflow_config.labels, workflow.build_environment)
    ciflow_ruleset.generate_json()
