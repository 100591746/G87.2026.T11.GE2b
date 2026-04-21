"""Module """
import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


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
            raise EnterpriseManagementException("File is not JSON formatted") from e

        if not isinstance(data, dict):
            raise EnterpriseManagementException("JSON does not have expected structure")







