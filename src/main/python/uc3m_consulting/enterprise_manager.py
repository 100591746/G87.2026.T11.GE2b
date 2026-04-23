"""Module."""
import json
import os
import re

from uc3m_consulting import ProjectDocument
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class EnterpriseManager:
    """Class for providing the methods for managing the orders."""

    def __init__(self):
        pass

    @staticmethod
    def validate_cif(_cif: str):
        """Return True if the CIF is valid."""
        return True

    @staticmethod
    def register_document(input_file: str):
        """Register a document for a project."""
        try:
            with open(input_file, "r", encoding="utf-8") as file_handler:
                content = file_handler.read()
        except FileNotFoundError as exc:
            raise EnterpriseManagementException("Input file not found") from exc

        keys = re.findall(r'"(PROJECT_ID|FILENAME)"\s*:', content)
        if keys.count("PROJECT_ID") > 1 or keys.count("FILENAME") > 1:
            raise EnterpriseManagementException("JSON does not have expected structure")

        try:
            data = json.loads(content)
        except json.JSONDecodeError as exc:
            raise EnterpriseManagementException("File is not JSON formatted") from exc

        if not isinstance(data, dict):
            raise EnterpriseManagementException("JSON does not have expected structure")

        expected_keys = {"PROJECT_ID", "FILENAME"}
        if set(data.keys()) != expected_keys:
            raise EnterpriseManagementException("JSON does not have expected structure")

        project_id = data["PROJECT_ID"]
        filename = data["FILENAME"]

        if not isinstance(project_id, str) or not isinstance(filename, str):
            raise EnterpriseManagementException("JSON data has no valid values")

        if not re.fullmatch(r"[0-9a-fA-F]{32}", project_id):
            raise EnterpriseManagementException("JSON data has no valid values")

        if not re.fullmatch(r"[a-zA-Z0-9]{8}\.(pdf|docx|xlsx)", filename):
            raise EnterpriseManagementException("JSON data has no valid values")

        try:
            document = ProjectDocument(project_id, filename)
            signature = EnterpriseManager._get_document_signature(document)
        except Exception as exc:
            raise EnterpriseManagementException(
                "Internal processing error when getting the file_signature"
            ) from exc

        documents = []
        all_documents_path = "all_documents.json"

        if os.path.exists(all_documents_path):
            try:
                with open(all_documents_path, "r", encoding="utf-8") as file_handler:
                    documents = json.load(file_handler)
            except (json.JSONDecodeError, OSError) as exc:
                raise EnterpriseManagementException(
                    "Internal processing error when getting the file_signature"
                ) from exc

        documents.append(document.to_json())

        try:
            with open(all_documents_path, "w", encoding="utf-8") as file_handler:
                json.dump(documents, file_handler, indent=2)
        except OSError as exc:
            raise EnterpriseManagementException(
                "Internal processing error when getting the file_signature"
            ) from exc

        return signature

    @staticmethod
    def _get_document_signature(document):
        """Get the document signature."""
        return document.document_signature
