This directory generates invocation test cases and executes them across releases, iteratively adjusting the tests while ensuring they target the intended API, to measure the deprecated API's **original-invocation failure version**.

The final cases are placed under:

```text
Benchmark/invocation_cases
```

---

## 1. Approach

1. Use [build_cases.py](build_cases.py) to call GPT-4o, generating initial invocation code from the library name, version, and FQN;
2. Manually review and correct these initial cases to obtain usable test cases;
3. Starting from the last version before the deprecation announcement (or the version before removal if the definition was already removed), execute the test cases across subsequent releases; the first release that makes the original invocation fail is the original-invocation failure version.

The script only produces the initial version; the actually used cases are the manually reviewed ones.

---

## 2. File Description

### `build_cases_input.xlsx`

The input workbook for `build_cases.py`: one worksheet per library, with column 1 as the version and column 2 as the deprecated API FQN.

### `build_cases.py`

The initial-generation script:

- reads an Excel workbook where each worksheet is a library, column 1 is the version, and column 2 is the FQN;
- calls GPT-4o (model `gpt-4o`) with the prompt in [prompt.txt](prompt.txt);
- writes the generated code to `bench_new` as `library / FQN@version / FQN.py`.

The paths `build_cases_input.xlsx`, `bench_new`, and `log.text` in the script are fixed paths from the development stage. The script reads `build_cases_input.xlsx` (one worksheet per library), taking column 1 as the version and column 2 as the deprecated API FQN.

### `prompt.txt`

The prompt template for GPT-4o, which asks for a minimal, complete, and independently executable code snippet that:

- actually calls the target API and prints the result;
- uses `inspect.getsource` to obtain the target API's source code, used later during manual review to confirm the invoked API is the target API;
- uses the common import and invocation style of that library version rather than calling the FQN directly;
- chooses appropriate test data to ensure the target API is invoked.

The template placeholders are `{library_name}`, `{version}`, and `{fully_qualified_name}`.

### `environment.yml`

The Conda environment (`LLMAPI`) required to run the script, with key dependencies `openai`, `pandas`, `openpyxl`, `python-dotenv`, etc. The API key and base URL are read from `.env` (`OPENAI_API_KEY`, `OPENAI_BASE_URL`).

---

## 3. Output

Initial structure:

```text
<output-directory>/<library>/<FQN>@<version>/<FQN>.py
```

The final, manually reviewed cases are organized by library under `Benchmark/invocation_cases`. Running these cases across releases yields each mapping's original-invocation failure version, which is written back to the `actual_invalid_version` column of `final_dataset.xlsx`.
