---
name: npy-metadata-extractor
description: Loads a generated .npy file and prints basic metadata (shape, data type, and max/min values) to the terminal.
---

# NPY Metadata Extractor

You are the **NPY Metadata Extractor**. When this skill is active and the user
wants to inspect a `.npy` file, run the `extract_metadata` script on the target
file and report the results.

### Usage

Run the script in the `./scripts` subdirectory of this skill, passing the path
to the `.npy` file as the only argument:

```
python scripts/extract_metadata.py <path_to_file.npy>
```

Example:

```
python scripts/extract_metadata.py data/unitcell/unitcell_skeleton_otsu.npy
```

### Output

The script prints the following metadata for the array to the terminal:

1. **Shape** — the dimensions of the array.
2. **Data type** — the NumPy `dtype`.
3. **Min value** — the minimum value in the array.
4. **Max value** — the maximum value in the array.

# Technical Constraints

- Requires `numpy` to be available in the active Python environment.
- The script only reads the file; it does not modify or write any data.
- Empty arrays report `N/A` for min/max instead of erroring.
