"""Tests for EnterpriseManager.register_document"""

import unittest
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
import tempfile
import os



class TestRegisterDocument(unittest.TestCase):
    """Functional tests for register_document"""

    def setUp(self):
        self.manager = EnterpriseManager()

    def test_tcf2_04_input_file_not_found(self):
        """TCF2_04 Input file path does not exist"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_document("does_not_exist.json")

    """Functional tests for register_document"""

    def setUp(self):
        """Create isolated temp workspace for each test"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        self.addCleanup(os.chdir, self.old_cwd)
        self.manager = EnterpriseManager()

    def _create_input_file(self, filename, content):
        """Helper to create test input files"""
        full_path = os.path.join(self.temp_dir.name, filename)
        with open(full_path, "w", encoding="utf-8") as file:
            file.write(content)
        return full_path

    def test_tcf2_04_input_file_not_found(self):
        """TCF2_04 Input file path does not exist"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_document("does_not_exist.json")

    def test_tcf2_05_missing_open_brace(self):
        """TCF2_05 JSON syntax error: missing opening brace"""
        content = (
            '"PROJECT_ID":"0123456789abcdef0123456789abcdef",'
            '"FILENAME":"AB12CD34.pdf"}'
        )
        input_file = self._create_input_file("f2_tc05_missing_open_brace.json", content)
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_document(input_file)


if __name__ == "__main__":
    unittest.main()