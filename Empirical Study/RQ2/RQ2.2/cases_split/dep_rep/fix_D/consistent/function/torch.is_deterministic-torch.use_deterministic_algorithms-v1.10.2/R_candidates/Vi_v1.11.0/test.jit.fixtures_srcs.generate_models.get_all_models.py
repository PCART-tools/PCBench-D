def get_all_models(model_directory_path: Path) -> Set[str]:
    files_in_fixtures = model_directory_path.glob('**/*')
    all_models_from_fixtures = [fixture.stem for fixture in files_in_fixtures if fixture.is_file()]
    return set(all_models_from_fixtures)
