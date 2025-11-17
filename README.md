# Axis Bank Document Verification Agent

An automated document verification system built with the Agno framework for Axis Bank. This agent verifies customer documents (Aadhaar, PAN, Passport, etc.) for various banking purposes like account opening, KYC, loan applications, and address updates.

## Features

- ✅ **Multi-document verification** - Supports Aadhaar, PAN, Passport, Utility bills, Salary slips, and more
- ✅ **OpenAI Vision API for image analysis** - Uses GPT-4 Vision for text extraction, field extraction, and tamper detection
- ✅ **Cross-document consistency checks** - Validates name and DOB across multiple documents
- ✅ **Tamper detection** - Identifies signs of document tampering
- ✅ **Confidence scoring** - Computes confidence scores for each document and overall submission
- ✅ **Structured output** - Returns machine-readable JSON for integration
- ✅ **PII protection** - Masks sensitive information in outputs
- ✅ **Human escalation** - Automatically escalates cases requiring manual review
- ✅ **Streamlit UI** - Ready-to-use web interface

## Architecture

Built using the **Agno framework** for multi-agent systems:
- Uses Agno's `Agent` class with structured outputs (Pydantic models)
- Implements custom tools for document verification
- Supports session storage and state management
- Compatible with OpenAI GPT and Anthropic Claude models

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up API keys:**
```bash
# For OpenAI
export OPENAI_API_KEY=your_key_here

# For Claude (optional)
export ANTHROPIC_API_KEY=your_key_here
```

3. **Note:** The system uses OpenAI Vision API (GPT-4o) for image analysis, so no additional OCR libraries are required. Just ensure your OpenAI API key is set.

## Usage

### Basic Usage

```python
from verification_agent import DocumentVerificationAgent

# Initialize agent
agent = DocumentVerificationAgent(
    model_id="gpt-4o-mini",
    storage_path="tmp/verification.db"  # Optional
)

# Verify documents
result = agent.verify_documents(
    purpose="account_opening_savings",
    file_paths=["pan.jpg", "aadhaar.jpg", "photo.jpg"],
    filenames=["pan.jpg", "aadhaar.jpg", "photo.jpg"],
    uploader_id="user_123"
)

# Get JSON output
json_output = agent.get_verification_result_json(result)

# Get user-friendly summary
summary = agent.get_user_summary(result)
print(summary)
```

### Streamlit UI

Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

The UI provides:
- Purpose selection
- Document upload interface
- Real-time verification
- Detailed results display
- JSON download

### Supported Purposes

- `account_opening_savings` - Open savings account
- `account_opening_salary` - Open salary account
- `address_update` - Update address
- `loan_application` - Loan application
- `credit_card_kyc` - Credit card KYC
- `business_account` - Open business account

## Document Types Supported

### Identity Documents
- Aadhaar card
- PAN card
- Passport
- Voter ID
- Driving License

### Address Proof
- Utility bills (electricity, water, gas)
- Bank statements
- Rent agreements

### Income Proof
- Salary slips
- Form 16
- ITR acknowledgement
- CA certificate

### Business Documents
- GST certificate
- Incorporation certificate
- Memorandum of Association

## Output Format

The agent returns a structured JSON object:

```json
{
  "request_id": "uuid",
  "timestamp": "2024-01-01T00:00:00Z",
  "purpose": "account_opening_savings",
  "required_documents": [...],
  "uploads": [...],
  "cross_checks": {
    "name_consistency": "MATCH",
    "dob_consistency": "MATCH",
    "face_match_score": null
  },
  "decision": "APPROVED",
  "decision_reasons": [...],
  "next_actions": [...],
  "audit": {...},
  "escalate_to_human": false
}
```

## Decision Logic

- **APPROVED**: Overall score ≥ 85%, all mandatory docs present, no tampering, consistency checks pass
- **REVIEW_REQUIRED**: Overall score 75-85%, or minor issues detected
- **REJECTED**: Overall score < 75%, missing mandatory docs, tampering detected, or consistency failures

## Security & Privacy

- ✅ PII masking in all outputs
- ✅ No external API calls to government servers
- ✅ Offline validation only (format checks, consistency)
- ✅ Audit trail for all operations
- ✅ Encrypted storage support (configure in production)

## Project Structure

```
axis_bank/
├── models.py                    # Pydantic models for structured output
├── document_requirements.py     # Document requirement mappings
├── verification_tools.py        # Document verification tools
├── verification_agent.py        # Main agent implementation
├── streamlit_app.py            # Streamlit UI
├── example_usage.py            # Usage examples
├── requirements.txt            # Dependencies
├── prompt.txt                  # System prompt (from requirements)
└── README.md                   # This file
```

## Development

### Running Examples

```bash
python example_usage.py
```

### Testing

```bash
# Install test dependencies
pip install pytest

# Run tests (when tests are added)
pytest tests/
```

## Integration with Streamlit

The `verify_documents_for_streamlit()` function in `verification_agent.py` is designed for easy Streamlit integration:

```python
import streamlit as st
from verification_agent import verify_documents_for_streamlit

uploaded_files = st.file_uploader("Upload documents", accept_multiple_files=True)

if st.button("Verify"):
    json_output, summary = verify_documents_for_streamlit(
        purpose="account_opening_savings",
        uploaded_files=uploaded_files,
        uploader_id=st.session_state.get("user_id")
    )
    st.json(json.loads(json_output))
    st.info(summary)
```

## Customization

### Adding New Document Types

1. Add document type to `DocumentType` enum in `models.py`
2. Update `detect_document_type()` in `verification_tools.py`
3. Add extraction logic in `extract_fields_from_document()`
4. Update document requirements in `document_requirements.py`

### Changing Decision Thresholds

Modify the `make_decision()` function in `verification_agent.py`:

```python
if overall_score >= 85:  # Change threshold
    decision = Decision.APPROVED
```

### Using Different Models

```python
# Use Claude
agent = DocumentVerificationAgent(
    model_id="claude-sonnet-4-20250514",
    use_claude=True
)

# Use GPT-4
agent = DocumentVerificationAgent(
    model_id="gpt-4",
    use_claude=False
)
```

## Limitations & Future Enhancements

- **Face Recognition**: Face matching not yet implemented. Add face recognition for photo verification.
- **PDF Support**: Currently optimized for images. Add PDF parsing support for multi-page documents.
- **Multi-language Support**: Add support for documents in regional languages (OpenAI Vision supports many languages).
- **Cloud Storage**: Add integration with cloud storage for document persistence.
- **Cost Optimization**: Consider caching OpenAI Vision API calls for repeated document types.

## License

Internal use for Axis Bank.

## Support

For issues or questions, contact the development team.

---

**Agent Version**: axis-docs-v1  
**Framework**: Agno  
**Last Updated**: 2024

