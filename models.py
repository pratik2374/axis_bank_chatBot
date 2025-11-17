"""Pydantic models for Axis Bank Document Verification Agent structured output."""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class DocumentType(str, Enum):
    """Supported document types."""
    AADHAAR = "Aadhaar"
    PAN = "PAN"
    PASSPORT = "Passport"
    VOTER_ID = "VoterID"
    DRIVING_LICENSE = "DrivingLicense"
    UTILITY_BILL = "Utility"
    BANK_STATEMENT = "BankStatement"
    SALARY_SLIP = "SalarySlip"
    FORM_16 = "Form16"
    ITR = "ITR"
    PHOTOGRAPH = "Photograph"
    SIGNATURE = "Signature"
    CHEQUE_LEAF = "ChequeLeaf"
    GST_CERTIFICATE = "GSTCertificate"
    INCORPORATION_CERTIFICATE = "IncorporationCertificate"
    OTHER = "Other"


class ConsistencyStatus(str, Enum):
    """Cross-document consistency status."""
    MATCH = "MATCH"
    PARTIAL = "PARTIAL"
    MISMATCH = "MISMATCH"


class Decision(str, Enum):
    """Verification decision."""
    APPROVED = "APPROVED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    REJECTED = "REJECTED"


class RequiredDocument(BaseModel):
    """Required document specification."""
    type: str = Field(..., description="Document type")
    required: bool = Field(..., description="Whether this document is mandatory")


class ExtractedFields(BaseModel):
    """Extracted fields from a document."""
    name: Optional[str] = Field(None, description="Name extracted from document")
    dob: Optional[str] = Field(None, description="Date of birth in YYYY-MM-DD format")
    document_number_masked: Optional[str] = Field(None, description="Masked document number")
    address: Optional[str] = Field(None, description="Address block")
    father_name: Optional[str] = Field(None, description="Father's name (for PAN)")
    nationality: Optional[str] = Field(None, description="Nationality (for Passport)")
    expiry_date: Optional[str] = Field(None, description="Expiry date in YYYY-MM-DD format")
    employer_name: Optional[str] = Field(None, description="Employer name (for salary slips)")
    salary: Optional[float] = Field(None, description="Salary/income figure")
    financial_year: Optional[str] = Field(None, description="Financial year")
    bill_date: Optional[str] = Field(None, description="Bill date (for utility bills)")


class DocumentUpload(BaseModel):
    """Information about an uploaded document."""
    upload_id: str = Field(..., description="Internal upload identifier")
    filename: str = Field(..., description="Original filename")
    detected_type: str = Field(..., description="Detected document type")
    extracted_fields: ExtractedFields = Field(..., description="Extracted fields from document")
    ocr_text_snippet: str = Field(..., description="First 120 chars of extracted text (masked)")
    confidence: int = Field(..., ge=0, le=100, description="Confidence score 0-100")
    tamper_flag: bool = Field(False, description="Whether tampering was detected")
    notes: List[str] = Field(default_factory=list, description="List of checks and results")


class CrossChecks(BaseModel):
    """Cross-document consistency checks."""
    name_consistency: ConsistencyStatus = Field(..., description="Name consistency across documents")
    dob_consistency: ConsistencyStatus = Field(..., description="DOB consistency across documents")
    face_match_score: Optional[int] = Field(None, ge=0, le=100, description="Face match score if applicable")


class Audit(BaseModel):
    """Audit trail information."""
    agent_version: str = Field(..., description="Agent version identifier")
    logs: List[str] = Field(default_factory=list, description="Step-by-step verification logs")
    consent_received: bool = Field(..., description="Whether user consent was received")


class VerificationResult(BaseModel):
    """Complete verification result matching the required JSON schema."""
    request_id: str = Field(..., description="UUID or timestamp-based request ID")
    timestamp: str = Field(..., description="ISO-8601 UTC timestamp")
    purpose: str = Field(..., description="User-selected purpose")
    required_documents: List[RequiredDocument] = Field(..., description="List of required documents")
    uploads: List[DocumentUpload] = Field(default_factory=list, description="List of uploaded documents")
    cross_checks: CrossChecks = Field(..., description="Cross-document consistency checks")
    decision: Decision = Field(..., description="Final verification decision")
    decision_reasons: List[str] = Field(default_factory=list, description="Human-readable decision reasons")
    next_actions: List[str] = Field(default_factory=list, description="Required next actions")
    audit: Audit = Field(..., description="Audit trail")
    escalate_to_human: bool = Field(False, description="Whether to escalate to human review")
    human_escalation_reason: Optional[str] = Field(None, description="Reason for human escalation")

    class Config:
        use_enum_values = True

