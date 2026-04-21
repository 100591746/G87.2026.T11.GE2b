"""Tests for EnterpriseManager.register_document"""

import unittest
from uc3m_consulting.enterprise_manager import EnterpriseManager
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class TestRegisterDocument(unittest.TestCase):
    """Functional tests for register_document"""

    def setUp(self):
        self.manager = EnterpriseManager()

    def test_tcf2_04_input_file_not_found(self):
        """TCF2_04 Input file path does not exist"""
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_document("does_not_exist.json")


if __name__ == "__main__":
    unittest.main()