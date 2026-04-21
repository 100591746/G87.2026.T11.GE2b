"""Module """
import json
import re
import os

from uc3m_consulting import ProjectDocument
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

        expected_keys = {"PROJECT_ID", "FILENAME"}

        # Must have exactly these two keys
        if set(data.keys()) != expected_keys:
            raise EnterpriseManagementException("JSON does not have expected structure")
        project_id = data["PROJECT_ID"]
        filename = data["FILENAME"]

        # Validate PROJECT_ID is a string
        if not isinstance(project_id, str):
            raise EnterpriseManagementException("JSON data has no valid values")

        # Validate FILENAME is a string
        if not isinstance(filename, str):
            raise EnterpriseManagementException("JSON data has no valid values")

        if not re.fullmatch(r"[0-9a-fA-F]{32}", project_id):
            raise EnterpriseManagementException("JSON data has no valid values")

        if not re.fullmatch(r"[a-zA-Z0-9]{8}\.(pdf|docx|xlsx)", filename):
            raise EnterpriseManagementException("JSON data has no valid values")

        try:
            document = ProjectDocument(project_id, filename)
            signature = EnterpriseManager._get_document_signature(document)
            document_json = document.to_json()
        except Exception as exc:
            raise EnterpriseManagementException(
                "Internal processing error when getting the file_signature"
            ) from exc

        documents = []
        all_documents_path = "all_documents.json"

        if os.path.exists(all_documents_path):
            try:
                with open(all_documents_path, "r", encoding="utf-8") as file:
                    documents = json.load(file)
            except (json.JSONDecodeError, OSError) as exc:
                raise EnterpriseManagementException(
                    "Internal processing error when getting the file_signature"
                ) from exc

        documents.append(document.to_json())

        try:
            with open(all_documents_path, "w", encoding="utf-8") as file:
                json.dump(documents, file, indent=2)
        except OSError as exc:
            raise EnterpriseManagementException(
                "Internal processing error when getting the file_signature"
            ) from exc

        try:
            with open(input_file, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError as e:
            raise EnterpriseManagementException("Input file not found") from e

        # Check for duplicate keys
        keys = re.findall(r'"(PROJECT_ID|FILENAME)"\s*:', content)
        if keys.count("PROJECT_ID") > 1 or keys.count("FILENAME") > 1:
            raise EnterpriseManagementException("JSON does not have expected structure")

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise EnterpriseManagementException("File is not JSON formatted") from e

        return signature

    @staticmethod
    def _get_document_signature(document):
        """Gets the document signature"""
        return document.document_signature


