"""Simple tool to call OpenAI Vision API with images."""

import base64
from pathlib import Path
from typing import Optional
from openai import OpenAI
from agno.tools import tool
from agno.agent import Agent

# Initialize OpenAI client
_client = None

def get_openai_client() -> OpenAI:
    """Get or create OpenAI client."""
    global _client
    if _client is None:
        _client = OpenAI()
    return _client


def encode_image_to_base64(file_path: str) -> str:
    """Encode image file to base64 string."""
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_image_mime_type(file_path: str) -> str:
    """Get MIME type from file extension."""
    ext = Path(file_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    return mime_types.get(ext, 'image/jpeg')


@tool
def analyze_document_image(
    agent: Agent,
    file_path: str,
    filename: Optional[str] = None,
    question: Optional[str] = None
) -> str:
    """
    Analyze a document image using OpenAI Vision API.
    
    This tool can:
    - Identify document type (Aadhaar, PAN, Passport, etc.)
    - Extract all relevant information (names, dates, numbers, addresses, etc.)
    - Verify document validity and format
    - Detect signs of tampering or editing
    - Check document quality
    
    Args:
        file_path: Path to the image file to analyze
        filename: Optional filename for context
        question: Optional specific question about the document (e.g., "Is this PAN card valid?")
        
    Returns:
        Detailed analysis of the document including type, extracted fields, validity, and any issues found.
    """
    try:
        client = get_openai_client()
        
        # Determine MIME type
        mime_type = get_image_mime_type(file_path)
        
        # Encode image
        base64_image = encode_image_to_base64(file_path)
        
        # Build prompt
        if question:
            prompt = f"""Analyze this document image and answer: {question}

Provide a comprehensive analysis including:
- Document type identification
- All extracted information (names, dates, document numbers, addresses, etc.)
- Validity checks
- Any issues or concerns
- Verification decision (APPROVED/REVIEW_REQUIRED/REJECTED)
- Confidence level
- Next steps if needed

IMPORTANT: Always mask sensitive information:
- Aadhaar numbers: Show as "xxxx-xxxx-1234" (last 4 digits only)
- PAN numbers: Show as "AB***1234C" (first 2, last 1, mask middle)
- Passport numbers: Show as "A****567" (first letter, last 3, mask middle)
- Account numbers: Show only last 4 digits

Be thorough and professional in your analysis."""
        else:
            prompt = """Analyze this document image comprehensively.

Provide a detailed analysis including:

1. **Document Type**: Identify what type of document this is (Aadhaar, PAN, Passport, Utility Bill, Salary Slip, etc.)

2. **Extracted Information**: Extract all relevant fields:
   - For identity documents: Name, DOB, Document number, Address (if applicable)
   - For PAN: Name, PAN number, DOB, Father's name (if visible)
   - For Aadhaar: Name, Aadhaar number, DOB, Address
   - For Passport: Name, Passport number, DOB, Nationality, Expiry date
   - For Utility bills: Customer name, Address, Bill date
   - For Salary slips: Employer name, Employee name, Salary amount, Period

3. **Validity Checks**:
   - Format validation (e.g., PAN format: ABCDE1234F)
   - Date validity
   - Document authenticity indicators

4. **Quality Assessment**:
   - Image clarity
   - Text readability
   - Document completeness

5. **Tamper Detection**:
   - Signs of editing or manipulation
   - Inconsistent fonts or alignment
   - Suspicious artifacts

6. **Verification Decision**: 
   - APPROVED: Document is valid and authentic
   - REVIEW_REQUIRED: Minor issues or needs clarification
   - REJECTED: Major issues, tampering, or invalid format

7. **Confidence Level**: High/Medium/Low

8. **Issues Found**: List any problems or concerns

9. **Next Steps**: What should be done next

IMPORTANT SECURITY RULES:
- ALWAYS mask sensitive numbers:
  - Aadhaar: "xxxx-xxxx-1234" (show only last 4 digits)
  - PAN: "AB***1234C" (first 2 letters, last letter, mask middle)
  - Passport: "A****567" (first letter, last 3 digits, mask middle)
  - Account numbers: Show only last 4 digits
- Never display full sensitive identifiers in plain text
- Be professional and clear in your response"""
        
        # Call OpenAI Vision API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=2000
        )
        
        result = response.choices[0].message.content
        
        if filename:
            return f"Analysis of {filename}:\n\n{result}"
        return result
    
    except Exception as e:
        return f"Error analyzing document: {str(e)}. Please ensure the file path is correct and the image is accessible."
