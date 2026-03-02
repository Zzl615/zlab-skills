---
name: tapd-xls-to-md
description: Converts corrupted or binary XLS (BIFF8) files ending in `_tapd.xls` to Markdown bug lists or detailed reports. You MUST use this skill whenever the user asks to extract a "Bug List" or "Bug Detail" from an Excel export, needs to convert an XLS file to Markdown, or whenever `pandas` / `xlrd` fails with corruption errors on an `.xls` file (e.g. encountering `\x10\x30` or BIFF8 issues). Do not try to parse it with standard python excel libraries if these conditions match; trigger this skill immediately.
---

# TAPD XLS to Markdown Converter

This skill is designed for TAPD exports ending in `_tapd.xls` that are corrupted or binary XLS (BIFF8) files which standard libraries (like `pandas` or `xlrd`) cannot read. It scans the raw binary stream to identifying valid strings and structures.

It provides two modes of extraction:
1. **Simple List**: Extracts Title, ID, and generates a TAPD URL in a single line per bug.
2. **Detailed Report**: Extracts Title, Iteration, Description, and Comment, grouping bugs by Iteration.

## How to use it

### 1. Generate Simple Bug List
Use the `xls_to_md.py` script to generate a list of bugs formatted as: `Index: Title ID 【Title】 URL`.

```bash
python3 <skill_dir>/tapd-xls-to-md/scripts/xls_to_md.py <path_to_xls_file> > bug_list.md
```

### 2. Generate Detailed Bug Report
Use the `xls_to_detail.py` script to generate a detailed report formatted with Iteration headers, Titles, Descriptions, and Comments.

```bash
python3 <skill_dir>/tapd-xls-to-md/scripts/xls_to_detail.py <path_to_xls_file> > bug_detail.md
```

## Dependencies
- Python 3 (standard libraries `sys`, `struct`, `re` only). No pip packages required.
