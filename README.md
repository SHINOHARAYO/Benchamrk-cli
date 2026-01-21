# Velocicode 🚀

**Velocicode** is a high-performance command-line tool for benchmarking programming language speeds. It allows you to run standard algorithms across multiple languages and compare their execution time with professional, interactive reports.

## Features ✨

- **Multi-Language Support**: Benchmarks **Python**, **C++**, **Rust**, **Go**, **JavaScript** (Node.js), **Java**, and **C#** (.NET).
- **Smart Execution**:
  - **System Info**: Auto-detects your CPU, RAM, and OS.
  - **Dependency Check**: Automatically checks for compilers and skips missing languages.
- **Premium UI**:
  - Beautiful terminal output using the **Rich** library.
  - Rankings with Medals (🥇 🥈 🥉).
  - Relative Speed comparisons (e.g., `1.00x` vs `45.9x`).
- **Data Export**:
  - **JSON**: Raw data export for analysis.
  - **HTML**: Interactive reports with **Charts** for presentations.

## Installation

```bash
pip install velocicode
```

## Usage

### 1. Run Benchmarks

Run all benchmarks with default settings:

```bash
velocicode run
```

The tool will display your system information and check if you have the necessary compilers. If some are missing, it will ask if you want to proceed with the available ones.

Filter by specific algorithm or language:

```bash
# Run only Matrix Multiplication in Rust and Go
velocicode run --filter-algo matrix_mul --filter-lang rust,go
```

### 2. Generate Reports 📊

Export results to JSON or generate a visual HTML report:

```bash
velocicode run --html report.html --json results.json
```

Open `report.html` in your browser to see interactive bar charts!

### 3. Check Compilers

Velocicode relies on system compilers. Check what you have installed:

```bash
velocicode check
```

## Requirements

> [!IMPORTANT]
> This tool requires external compilers. `pip` installs the runner, but you need the languages installed:

- **Python 3.7+**
- `g++` (for C++)
- `rustc` (for Rust)
- `go` (for Go)
- `node` (for JavaScript)
- `javac` (for Java)
- `dotnet` (for C#)

## License

MIT
