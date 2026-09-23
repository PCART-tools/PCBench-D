RQ1 examines the relationship between deprecated APIs and their maintainer-specified replacements from two perspectives: where replacements are located relative to deprecated APIs, which informs candidate search scopes; and, once a replacement is identified, the parameter-interface differences between them that may affect invocation adaptation.

RQ1 is divided into two sub-questions:

- **RQ1.1 Replacement Locality:** Analyzes the source-definition location relationship between deprecated and replacement APIs.
- **RQ1.2 Parameter-Interface Differences:** Analyzes parameter-interface changes between deprecated and replacement APIs.


## Data and Version Selection

Both sub-questions use the same version pair:

- **Deprecated API:** The final pre-announcement release (or the release before removal if the definition was already removed).
- **Replacement API:** The announcement release.

RQ1.1 compares the source-definition FQNs across these two versions; RQ1.2 compares the parameter signatures of functions, methods, or classes in the same versions.

Each sub-question processes `class`, `function`, and `method` granularities separately:

```text
RQ1.1/
├── input/
├── output/
└── fqn_classify.py

RQ1.2/
├── input/
├── output/
└── do_analyze.py
```


## Analysis Workflow

The RQ1 workflow is:

```text
RQ1.1 input/*.xlsx
        │
        └── fqn_classify.py
                └── FQN locality classification results

RQ1.2 input/*.xlsx
        │
        └── do_analyze.py + PCART
                └── parameter-interface difference results
```

The two sub-questions are independent: RQ1.1 focuses on API definition location, while RQ1.2 focuses on parameter interfaces. RQ1.2 does not require RQ1.1's classification results as input.


## Result Interpretation

### RQ1.1

RQ1.1 reports FQN-locality category counts and proportions separately for class, function, and method mappings. Detailed classification rules and output labels are described in [RQ1.1/README.md](RQ1.1/README.md).

### RQ1.2

RQ1.2 reports parameter-interface differences by API granularity, including the distribution of mappings by the number of change types and the detailed results for mappings with a single change type. The parameter-change categories and exclusion criteria are described in [RQ1.2/README.md](RQ1.2/README.md).


## Subdirectory Descriptions

- [RQ1.1/README.md](RQ1.1/README.md): FQN locality classification method, inputs/outputs, and classification results.
- [RQ1.2/README.md](RQ1.2/README.md): Parameter-interface difference analysis, PCART invocation, and output results.
