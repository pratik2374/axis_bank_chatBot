"""Example usage of the Axis Bank Document Verification Agent."""

from pathlib import Path
from verification_agent import DocumentVerificationAgent
from document_requirements import get_required_documents, get_purpose_display_name


def main():
    """Example usage of the verification agent."""
    
    # Initialize the agent
    agent = DocumentVerificationAgent(
        model_id="gpt-4o-mini",  # Use a cheaper model for testing
        storage_path="tmp/axis_verification.db"  # Optional: persist sessions
    )
    
    # Example 1: Account opening with sample documents
    print("=" * 60)
    print("Example: Account Opening (Savings)")
    print("=" * 60)
    
    # In a real scenario, these would be actual uploaded files
    # For demo, we'll use placeholder file paths
    # You would replace these with actual file paths from uploads
    
    purpose = "account_opening_savings"
    
    # Show required documents
    required_docs = get_required_documents(purpose)
    print(f"\nPurpose: {get_purpose_display_name(purpose)}")
    print("\nRequired Documents:")
    for doc in required_docs:
        status = "MANDATORY" if doc.required else "OPTIONAL"
        print(f"  - {doc.type}: {status}")
    
    # Example file paths (replace with actual uploaded files)
    # file_paths = [
    #     "uploads/pan_card.jpg",
    #     "uploads/aadhaar_card.jpg",
    #     "uploads/photograph.jpg",
    #     "uploads/utility_bill.pdf"
    # ]
    # filenames = [
    #     "pan_card.jpg",
    #     "aadhaar_card.jpg",
    #     "photograph.jpg",
    #     "utility_bill.pdf"
    # ]
    
    # For demo purposes, we'll create a mock result
    print("\n" + "=" * 60)
    print("Note: To actually verify documents, provide real file paths")
    print("=" * 60)
    print("\nExample code:")
    print("""
    result = agent.verify_documents(
        purpose="account_opening_savings",
        file_paths=["path/to/pan.jpg", "path/to/aadhaar.jpg"],
        filenames=["pan.jpg", "aadhaar.jpg"],
        uploader_id="user_123"
    )
    
    # Get JSON output (for Streamlit backend)
    json_output = agent.get_verification_result_json(result)
    
    # Get user-friendly summary
    summary = agent.get_user_summary(result)
    
    print(json_output)
    print("\\n" + summary)
    """)
    
    # Example 2: Show different purposes
    print("\n" + "=" * 60)
    print("Available Purposes:")
    print("=" * 60)
    
    purposes = [
        "account_opening_savings",
        "account_opening_salary",
        "address_update",
        "loan_application",
        "credit_card_kyc",
        "business_account",
    ]
    
    for purpose in purposes:
        print(f"\n{purpose}:")
        docs = get_required_documents(purpose)
        for doc in docs:
            status = "✓" if doc.required else "○"
            print(f"  {status} {doc.type}")


if __name__ == "__main__":
    main()

