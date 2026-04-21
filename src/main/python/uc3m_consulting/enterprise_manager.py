"""Module """
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
import json
class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(cif: str):
        """RETURNs TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True

    @staticmethod
    def register_document(input_file: str):
        """Registers a document for a project by validating the input file,
        computing a SHA-256 signature, and storing the result."""
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise EnterpriseManagementException("Input file not found") from e
        except json.JSONDecodeError as e:
            raise EnterpriseManagementExceptionoka

    def test_tcf2_09_array_root(self):
        """TCF2_09 Top-level JSON is array instead of object"""
        content = (
            '[{"PROJECT_ID":"0123456789abcdef0123456789abcdef",'
            '"FILENAME":"AB12CD34.pdf"}]'
        )
        input_file = self._create_input_file("f2_tc09_array_root.json", content)
        with self.assertRaises(EnterpriseManagementException):
            self.manager.register_document(input_file)






