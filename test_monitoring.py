import unittest
import os
import csv
import io
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import monitoring


class TestMonitoring(unittest.TestCase):
    def setUp(self):
        self.test_storage = "test_measurements.csv"
        if os.path.exists(self.test_storage):
            os.remove(self.test_storage)

    def tearDown(self):
        if os.path.exists(self.test_storage):
            os.remove(self.test_storage)

    @patch("monitoring.psutil")
    def test_measure_records_data(self, mock_psutil):
        # Mock psutil values
        mock_psutil.cpu_percent.return_value = 10.5
        mock_psutil.virtual_memory.return_value.percent = 50.0

        monitoring.measure(["cpu_percent", "virtual_memory"], self.test_storage)

        self.assertTrue(os.path.exists(self.test_storage))
        with open(self.test_storage, "r") as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 2)
            self.assertEqual(reader[0]["metric"], "cpu_percent")
            self.assertEqual(float(reader[0]["value"]), 10.5)
            self.assertEqual(reader[1]["metric"], "virtual_memory")
            self.assertEqual(float(reader[1]["value"]), 50.0)

    @patch("monitoring.psutil")
    def test_measure_clean_option(self, mock_psutil):
        mock_psutil.cpu_percent.return_value = 10.5
        
        # First measurement
        monitoring.measure(["cpu_percent"], self.test_storage)
        
        # Second measurement with clean=True
        monitoring.measure(["cpu_percent"], self.test_storage, clean=True)

        with open(self.test_storage, "r") as f:
            reader = list(csv.DictReader(f))
            # Should only have 1 entry because of clean
            self.assertEqual(len(reader), 1)

    def test_report_filtering(self):
        # Setup dummy data
        now = datetime.now()
        past = now - timedelta(hours=1)
        future = now + timedelta(hours=1)

        with open(self.test_storage, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "metric", "value"])
            writer.writerow([past.strftime("%Y-%m-%d %H:%M:%S"), "cpu", "10"])
            writer.writerow([now.strftime("%Y-%m-%d %H:%M:%S"), "cpu", "20"])
            writer.writerow([future.strftime("%Y-%m-%d %H:%M:%S"), "cpu", "30"])

        # Test filtering by start time
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            monitoring.report(self.test_storage, start_time=now.strftime("%Y-%m-%d %H:%M:%S"))
            output = fake_out.getvalue()
            self.assertIn("20.00", output)
            self.assertIn("30.00", output)
            self.assertNotIn("10.00", output)

    def test_report_stats(self):
        with open(self.test_storage, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "metric", "value"])
            writer.writerow(["2026-03-11 10:00:00", "cpu", "10"])
            writer.writerow(["2026-03-11 10:01:00", "cpu", "20"])

        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            monitoring.report(self.test_storage, show_avg=True, show_total=True)
            output = fake_out.getvalue()
            self.assertIn("Avg: 15.00", output)
            self.assertIn("Total: 30.00", output)

    def test_parse_datetime_formats(self):
        dt = monitoring.parse_datetime("2026-03-11 10:00:00")
        self.assertEqual(dt.year, 2026)
        self.assertEqual(dt.hour, 10)

        dt = monitoring.parse_datetime("2026-03-11")
        self.assertEqual(dt.year, 2026)
        self.assertEqual(dt.hour, 0)

        with self.assertRaises(ValueError):
            monitoring.parse_datetime("invalid-date")


if __name__ == "__main__":
    unittest.main()
