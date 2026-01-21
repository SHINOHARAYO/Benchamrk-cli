# Benchmark CLI

A command-line interface tool to benchmark the execution speed of various programming languages (Python, C++, Rust, Go, JavaScript) on standard algorithms.

## Installation

```bash
pip install benchmark-cli
```

## Platform Support

- **Linux**: Fully supported.
- **macOS**: Fully supported (requires Xcode Command Line Tools for compilers).
- **Windows**: Supported via **WSL2** (Windows Subsystem for Linux). Native Windows support is currently experimental.

## Usage

Run the interactive mode:

```bash
benchmark-cli
```

Or use command line arguments:

```bash
# Run all
benchmark-cli run

# Filter by algorithm
benchmark-cli run --filter-algo matrix_mul

# Filter by language
benchmark-cli run --filter-lang python,cpp
```

## Supported Benchmarks

- **Fibonacci**
- **Matrix Multiplication**
- **Quick Sort**

## Requirements

> [!IMPORTANT]
> This tool requires external compilers to be installed on your system. `pip` will **not** install these for you.

- Python 3.7+
- **System Compilers**:
  - `python3` (for Python)
  - `g++` (for C++)
  - `rustc` (for Rust)
  - `go` (for Go)
  - `node` (for JavaScript)

Run `benchmark-cli check` to see which compilers are missing on your system. The tool will simply skip languages that are not installed.
