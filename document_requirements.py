"""Document requirement mappings based on purpose."""

from typing import Dict, List, Tuple
from models import RequiredDocument


# Mapping of purpose to required documents
DOCUMENT_REQUIREMENTS: Dict[str, List[Tuple[str, bool]]] = {
    "account_opening_savings": [
        ("PAN", True),
        ("Aadhaar", True),
        ("Photograph", True),
        ("Utility", False),  # One of address proof is mandatory
        ("BankStatement", False),  # One of address proof is mandatory
    ],
    "account_opening_salary": [
        ("PAN", True),
        ("Aadhaar", True),
        ("Photograph", True),
        ("SalarySlip", True),
        ("Utility", False),  # One of address proof is mandatory
        ("BankStatement", False),  # One of address proof is mandatory
    ],
    "address_update": [
        ("Aadhaar", False),  # One identity doc required
        ("PAN", False),  # One identity doc required
        ("Utility", False),  # One address proof required
        ("BankStatement", False),  # One address proof required
    ],
    "loan_application": [
        ("PAN", True),
        ("Aadhaar", True),
        ("SalarySlip", False),  # Income proof required (one of)
        ("Form16", False),  # Income proof required (one of)
        ("ITR", False),  # Income proof required (one of)
    ],
    "credit_card_kyc": [
        ("PAN", True),
        ("Aadhaar", True),
        ("SalarySlip", False),  # Required if applying above threshold
        ("Form16", False),  # Required if applying above threshold
    ],
    "business_account": [
        ("PAN", True),  # Business PAN
        ("GSTCertificate", True),
        ("IncorporationCertificate", True),
        ("Aadhaar", True),  # KYC of signatories
    ],
}


def get_required_documents(purpose: str) -> List[RequiredDocument]:
    """
    Get list of required documents for a given purpose.
    
    Args:
        purpose: The purpose string (e.g., "account_opening_savings")
        
    Returns:
        List of RequiredDocument objects
    """
    if purpose not in DOCUMENT_REQUIREMENTS:
        # Default: return common KYC documents
        return [
            RequiredDocument(type="PAN", required=True),
            RequiredDocument(type="Aadhaar", required=True),
        ]
    
    return [
        RequiredDocument(type=doc_type, required=required)
        for doc_type, required in DOCUMENT_REQUIREMENTS[purpose]
    ]


def get_purpose_display_name(purpose: str) -> str:
    """Get human-readable purpose name."""
    mapping = {
        "account_opening_savings": "Open Savings Account",
        "account_opening_salary": "Open Salary Account",
        "address_update": "Update Address",
        "loan_application": "Loan Application",
        "credit_card_kyc": "Credit Card KYC",
        "business_account": "Open Business Account",
    }
    return mapping.get(purpose, purpose.replace("_", " ").title())

