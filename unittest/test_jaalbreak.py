import unittest
from unittest.mock import patch, MagicMock
import os
from mainclitest import (
    validate_nmap,
    export_to_pdf,
    prompt_intensity,
    run_nmap_command,
    advanced_scan,
)

class TestJaalBreakCLI(unittest.TestCase):

    def test_validate_nmap(self):
        with patch('shutil.which', return_value='/usr/bin/nmap'):
            self.assertTrue(validate_nmap())
            print("✅ validate_nmap() correctly detects installed nmap")
        with patch('shutil.which', return_value=None):
            self.assertFalse(validate_nmap())
            print("✅ validate_nmap() correctly detects missing nmap")

    def test_export_to_pdf(self):
        sample_text = "Host is up.\nScan complete."
        test_file = "test_output.pdf"
        export_to_pdf(sample_text, test_file)
        self.assertTrue(os.path.exists(test_file))
        os.remove(test_file)
        print("✅ export_to_pdf() generates a valid PDF with content")

    def test_export_to_pdf_logo_missing(self):
        sample_text = "Scan Output with missing logo"
        test_file = "test_missing_logo.pdf"
        with patch('os.path.join', return_value="non_existent_logo.png"):
            export_to_pdf(sample_text, test_file)
            self.assertTrue(os.path.exists(test_file))
            os.remove(test_file)
            print("✅ export_to_pdf() handles missing logo image gracefully")

    def test_prompt_intensity_valid(self):
        with patch('builtins.input', side_effect=["1"]):
            with patch('builtins.print') as mocked_print:
                self.assertEqual(prompt_intensity(), "-T1")
                printed_lines = [str(call.args[0]) for call in mocked_print.call_args_list]
                self.assertTrue(any("Intensity level set to: -T1" in line for line in printed_lines))
                print("✅ prompt_intensity() accepts and confirms valid input")

    def test_prompt_intensity_invalid_then_valid(self):
        with patch('builtins.input', side_effect=["abc", "6", "2"]):
            with patch('builtins.print') as mocked_print:
                self.assertEqual(prompt_intensity(), "-T2")
                printed_lines = [str(call.args[0]) for call in mocked_print.call_args_list]
                self.assertGreaterEqual(printed_lines.count("[!] Invalid intensity level."), 2)
                self.assertTrue(any("Intensity level set to: -T2" in line for line in printed_lines))
                print("✅ prompt_intensity() retries until valid input is given")

    def test_prompt_intensity_skip(self):
        with patch('builtins.input', side_effect=[""]):
            with patch('builtins.print') as mocked_print:
                self.assertIsNone(prompt_intensity())
                printed_lines = [str(call.args[0]) for call in mocked_print.call_args_list]
                self.assertTrue(any("Skipping intensity selection." in line for line in printed_lines))
                print("✅ prompt_intensity() skips when input is empty")

    def test_run_nmap_command_success(self):
        mock_popen = MagicMock()
        mock_popen.stdout = iter(["Host is up.\n", "Scan complete.\n"])
        mock_popen.wait = MagicMock()
        mock_popen.returncode = 0
        with patch('subprocess.Popen', return_value=mock_popen):
            result = run_nmap_command(["nmap", "-sn", "127.0.0.1"])
            self.assertIn("Host is up", result)
            self.assertIn("Scan complete", result)
            print("✅ run_nmap_command() captures successful scan output")

    def test_run_nmap_command_failure(self):
        mock_popen = MagicMock()
        mock_popen.stdout = iter([""])
        mock_popen.wait = MagicMock()
        mock_popen.returncode = 1
        with patch('subprocess.Popen', return_value=mock_popen):
            result = run_nmap_command(["nmap", "-sn", "invalid"])
            self.assertIn("Error: Execution failed", result)
            print("✅ run_nmap_command() handles and reports command failure")

    def test_conflict_ping_scan_with_others(self):
        with patch('builtins.input', side_effect=["127.0.0.1", "", "2,3"]):
            with patch('builtins.print') as mocked_print:
                advanced_scan()
                printed_lines = [str(call.args[0]) for call in mocked_print.call_args_list]
                self.assertTrue(any("Ping Scan cannot be combined" in line for line in printed_lines))
                print("✅ Conflict validation: Ping Scan + Others was rejected")

    def test_conflict_quick_scan_with_port_scan(self):
        with patch('builtins.input', side_effect=["127.0.0.1", "", "1,3"]):
            with patch('builtins.print') as mocked_print:
                advanced_scan()
                printed_lines = [str(call.args[0]) for call in mocked_print.call_args_list]
                self.assertTrue(any("Quick Scan and Port Scan cannot be combined" in line for line
                                    in printed_lines))
                print("✅ Conflict validation: Quick Scan + Port Scan was rejected")

if __name__ == '__main__':
    unittest.main(verbosity=2)
