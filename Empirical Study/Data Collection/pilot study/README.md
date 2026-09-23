The pilot study determines the screening scope and retrieval keywords for formal collection: it identifies the common **dedicated deprecation-related sections** in changelogs and the **deprecation-related keywords**.

---

## 1. Data

It covers 33 libraries, collecting each library's version numbers up to 2025-03-18, then uses the script [random_version.py](../random_version.py) to randomly sample 5 versions per library (fixed random seed 2025, no duplicate versions), yielding **165 changelogs** in total.

The sampling results are recorded in:

[library versions & randomly selected versions.xlsx](library%20versions%20%26%20randomly%20selected%20versions.xlsx)

- `change logs source`: changelog sources for each library;
- `library versions & randomly selected versions`: version lists and randomly sampled versions per library.

---

## 2. Process

1. Collect each library's version numbers;
2. Randomly sample 5 versions per library;
3. Manually collect the dedicated deprecation-related sections and deprecation-related entries from these 165 versions;
4. For the deprecation-related entries, two researchers independently pick out deprecation keywords and merge the retained keywords after resolving disagreements.

---

## 3. Results

### Dedicated deprecation-related sections

Recorded in:

[the incompatible changes section among 165 versions.xlsx](the%20incompatible%20changes%20section%20among%20165%20versions.xlsx)

Columns: `library`, `versions`, `whether the Incompatible Changes section is included`.

Only 38 of the 165 changelogs have a dedicated deprecation-related section, so during formal collection: entries in dedicated sections are screened one by one, and keyword retrieval is used elsewhere.

### Deprecation keywords

Recorded in:

[deprecation related keyword statistics.xlsx](deprecation%20related%20keyword%20statistics.xlsx)

Main columns: `version`, `entries for deprecation changes`, `section`, `keyword`, plus a `keywords analysis` worksheet that summarizes keyword coverage.

Annotation results: Jaccard similarity **0.852**, Cohen's kappa **0.907**; after merging word forms, **15 stems** were retained, covering **99.46%** of the pilot entries.
