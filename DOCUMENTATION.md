# System Monitor CLI

A command-line tool for monitoring system metrics, storing them in a persistent format, and generating reports with statistical analysis.

## Requirements

- Python 3.x
- `psutil` library

To install requirements:
```bash
pip install psutil
```

## Supported Metrics

- `cpu_percent`: Current system-wide CPU utilization as a percentage.
- `virtual_memory`: Percentage of used virtual memory.
- `disk_usage`: Percentage of used disk space on the root partition.
- `swap_memory`: Percentage of used swap memory.

## Usage

The application uses subcommands: `measure`, `report`, and `clean`.

### 1. Measuring Metrics

Performs measurements and adds them to the storage file (default: `measurements.csv`).

**Command:**
```bash
python monitoring.py measure [METRICS...] [--storage PATH] [--clean]
```

**Examples:**
- Record CPU and Memory:
  ```bash
  python monitoring.py measure cpu_percent virtual_memory
  ```
- Clear existing data and record disk usage:
  ```bash
  python monitoring.py measure disk_usage --clean
  ```

### 2. Generating Reports

Reads stored measurements and displays them in a formatted table. Supports filtering and basic statistics.

**Command:**
```bash
python monitoring.py report [--start START_TIME] [--end END_TIME] [--metrics METRICS...] [--avg] [--total]
```

- `--start` / `--end`: Format `YYYY-MM-DD` or `YYYY-MM-DD HH:MM:SS`.
- `--avg`: Show average for each metric.
- `--total`: Show sum for each metric.

**Examples:**
- View all data recorded today:
  ```bash
  python monitoring.py report --start 2026-03-11
  ```
- View CPU stats for a specific time range:
  ```bash
  python monitoring.py report --start "2026-03-11 10:00:00" --end "2026-03-11 11:00:00" --metrics cpu_percent --avg
  ```

### 3. Cleaning Data

Manually clear the storage file.

```bash
python monitoring.py clean
```

### 4. Using Configuration Files

You can pass arguments from a file by prefixing the filename with `@`.

**Example `config.txt`:**
```text
measure
cpu_percent
virtual_memory
--storage custom_data.csv
```

**Run it:**
```bash
python monitoring.py @config.txt
```

## Running Tests

To verify the installation and functionality:
```bash
python test_monitoring.py
```
