# Ghost Collar Merger 👻

A desktop GUI tool for processing pipe inspection data by merging ghost collar intervals and exporting the results to Excel.

## What It Does

In tubing inspection logs, ghost collars are false signal artifacts that appear between real defect intervals. This tool identifies and merges those intervals based on a configurable collar length threshold, producing a clean, consolidated output ready for reporting.

## Features

- Load SmartLog Joint Analysis CSV files
- Set a custom ghost collar length threshold (ft)
- Merges intervals where the gap between joints meets or exceeds the threshold
- Preserves comment labels (e.g. "Pup Joint") over numeric MaxLoss% values
- Exports merged results to a formatted `.xlsx` Excel file

## Requirements

- Python 3.x
- `pandas`
- `openpyxl`
- `tkinter` (included with standard Python)

Install dependencies:
```bash
pip install pandas openpyxl
```

## Usage

```bash
python ghostMerge.py
```

1. Enter the ghost collar length threshold (default: 3 ft)
2. Click **Select CSV and Merge** and choose your input file
3. Choose where to save the output Excel file
4. Click **Open Output Folder** to navigate to the saved file

## Input Format

Expects a SmartLog JointAnalysis CSV with 2 header rows followed by columns including:
`Top`, `Bottom`, `Length`, `TNom`, `TMin`, `MaxLoss%`, `DptMxLos`, `Comment`

## Output Columns

| Column | Description |
|--------|-------------|
| Top | Top depth of interval |
| Bottom | Bottom depth of interval |
| Length | Interval length |
| TNom | Nominal wall thickness |
| TMin | Minimum wall thickness in group |
| DptMxLos | Depth of maximum loss |
| MaxLoss% | Max loss % or comment label if present |
| Source | `original` or `merged (ghost collar chain)` |

## License

This project is licensed under the [MIT License](LICENSE).

> This software is provided for research, educational, and informational purposes only. The authors make no warranties of any kind and shall not be held liable for any damages arising from its use. See [LICENSE](LICENSE) for the full disclaimer.
