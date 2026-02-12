---
name: tapd-xls-to-md
description: Converts corrupted or binary XLS (BIFF8) files ending in `_tapd.xls` to Markdown bug lists or detailed reports. Use this when standard tools fail to read an XLS file or when specific bug report formatting (list or detail) is required.
---

# TAPD XLS to Markdown Converter

This skill is designed for TAPD exports ending in `_tapd.xls` that are corrupted or binary XLS (BIFF8) files which standard libraries (like `pandas` or `xlrd`) cannot read. It scans the raw binary stream to identifying valid strings and structures.

It provides two modes of extraction:
1. **Simple List**: Extracts Title, ID, and generates a TAPD URL in a single line per bug.
2. **Detailed Report**: Extracts Title, Iteration, Description, and Comment, grouping bugs by Iteration.

## When to use this skill

- **When the file name ends with `_tapd.xls`.**
- When you need to convert an XLS file to a Markdown document.
- When `pandas.read_excel()` or `xlrd.open_workbook()` fails with corruption errors on an `.xls` file.
- Claims to extract "Bug List" or "Bug Detail" from an Excel export.
- When you see byte patterns like `\x10\x30` (【) in a file but cannot decode it globally.

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
