"""
System Monitor - A CLI tool for monitoring system metrics.
Supports measuring metrics, storing them with timestamps, and reporting results.
"""

import argparse
import csv
import os
import sys
from datetime import datetime

import psutil

DEFAULT_STORAGE = "measurements.csv"


def get_timestamp():
    """Return the current timestamp as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def parse_datetime(dt_str):
    """Parse a datetime string into a datetime object."""
    try:
        return datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        try:
            return datetime.strptime(dt_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date format: {dt_str}. Use YYYY-MM-DD HH:MM:SS or YYYY-MM-DD")


def get_metric_value(name):
    """Return the value of the specified metric using psutil."""
    if name == "cpu_percent":
        return psutil.cpu_percent(interval=1)
    elif name == "virtual_memory":
        return psutil.virtual_memory().percent
    elif name == "disk_usage":
        return psutil.disk_usage("/").percent
    elif name == "swap_memory":
        return psutil.swap_memory().percent
    else:
        raise ValueError(f"Unknown metric: {name}")


def measure(metrics, storage_file, clean=False):
    """Measure the specified metrics and save them to storage."""
    if clean and os.path.exists(storage_file):
        os.remove(storage_file)

    write_header = not os.path.exists(storage_file)

    with open(storage_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp", "metric", "value"])

        timestamp = get_timestamp()
        for name in metrics:
            try:
                value = get_metric_value(name)
                writer.writerow([timestamp, name, value])
                print(f"Recorded {name}: {value} at {timestamp}")
            except ValueError as e:
                print(f"Error measuring {name}: {e}", file=sys.stderr)


def report(storage_file, start_time=None, end_time=None, metrics=None,
           show_avg=False, show_total=False):
    """Read and display stored measurements within the time range."""
    if not os.path.exists(storage_file):
        print(f"No measurements found in {storage_file}")
        return

    start_dt = parse_datetime(start_time) if start_time else None
    end_dt = parse_datetime(end_time) if end_time else None

    results = []
    with open(storage_file, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row_dt = parse_datetime(row["timestamp"])
            except ValueError:
                continue
            if start_dt and row_dt < start_dt:
                continue
            if end_dt and row_dt > end_dt:
                continue
            if metrics and row["metric"] not in metrics:
                continue
            row["value"] = float(row["value"])
            results.append(row)

    if not results:
        print("No measurements match the criteria.")
        return

    print(f"{'Timestamp':<20} | {'Metric':<20} | {'Value':<10}")
    print("-" * 56)
    for row in results:
        print(f"{row['timestamp']:<20} | {row['metric']:<20} | {row['value']:<10.2f}")

    if show_avg or show_total:
        print("-" * 56)
        stats = {}
        for row in results:
            m = row["metric"]
            if m not in stats:
                stats[m] = []
            stats[m].append(row["value"])

        for m, values in stats.items():
            line = f"Stats for {m}:"
            if show_avg:
                avg = sum(values) / len(values)
                line += f" Avg: {avg:.2f}"
            if show_total:
                total = sum(values)
                line += f" Total: {total:.2f}"
            print(line)


def main():
    parser = argparse.ArgumentParser(
        description="System Monitor - Resource Tracking",
        fromfile_prefix_chars="@"
    )
    parser.add_argument("--storage", default=DEFAULT_STORAGE, help="Path to CSV storage")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Measure subcommand
    measure_p = subparsers.add_parser("measure", help="Perform measurements")
    measure_p.add_argument("metrics", nargs="+", help="Metric names to measure (cpu_percent, virtual_memory, etc.)")
    measure_p.add_argument("--clean", action="store_true", help="Clear storage before measuring")

    # Report subcommand
    report_p = subparsers.add_parser("report", help="Report stored measurements")
    report_p.add_argument("--start", help="Start time (YYYY-MM-DD [HH:MM:SS])")
    report_p.add_argument("--end", help="End time (YYYY-MM-DD [HH:MM:SS])")
    report_p.add_argument("--metrics", nargs="*", help="Specific metrics to report (default: all)")
    report_p.add_argument("--avg", action="store_true", help="Calculate average")
    report_p.add_argument("--total", action="store_true", help="Calculate total")

    # Clean subcommand (extra utility)
    subparsers.add_parser("clean", help="Clear stored measurements")

    args = parser.parse_args()

    if args.command == "measure":
        measure(args.metrics, args.storage, args.clean)
    elif args.command == "report":
        report(args.storage, args.start, args.end, args.metrics, args.avg, args.total)
    elif args.command == "clean":
        if os.path.exists(args.storage):
            os.remove(args.storage)
            print(f"Removed {args.storage}")
        else:
            print("Storage file does not exist.")


if __name__ == "__main__":
    main()
