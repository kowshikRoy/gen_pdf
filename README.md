# Code to PDF Generator

This script generates a PDF file from source code files in a directory, with syntax highlighting.

## Prerequisites

- Python 3.x
- `pip` for installing packages

## Installation

1.  Clone the repository or download the files.
2.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To generate a PDF, run the `gen_pdf.py` script with the following arguments:

```bash
python gen_pdf.py <directory> -e <extensions> [-o <output_filename>] [--exclude-suffix <suffixes>]
```

### Arguments

-   `directory`: The path to the directory containing the source code files.
-   `-e`, `--extensions`: A list of file extensions to include (e.g., `.py .js .html`).
-   `-o`, `--output`: The name of the output PDF file (default: `output.pdf`).
-   `--exclude-suffix`: A list of file suffixes to exclude (e.g., `_test.go .spec.js`).

### Example

To generate a PDF named `my_project.pdf` from all `.py` and `.js` files in the `my_project` directory, excluding test files:

```bash
python gen_pdf.py ./my_project -e .py .js -o my_project.pdf --exclude-suffix _test.py .test.js
