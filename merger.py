import json
import os

def load_document_from_db(doc_id):
    """
    Simulates fetching a document from a database using its ID.
    In this example, it just reads from a local JSON file.
    The filename is assumed to be the document ID + '.json'.
    """
    filename = f"{doc_id}.json"
    if not os.path.exists(filename):
        print(f"Error: Document '{filename}' not found.")
        return None
    
    with open(filename, 'r') as f:
        return json.load(f)

def resolve_and_merge_document(primary_doc_id):
    """
    Resolves and merges a primary document with its child chunks.
    
    1. Fetches the primary document.
    2. Checks for child document pointers.
    3. Fetches each child document.
    4. Concatenates the content into a final, merged object.
    """
    print(f"--- Starting merge process for: {primary_doc_id} ---")
    
    # 1. Fetch the primary document
    primary_doc = load_document_from_db(primary_doc_id)
    if not primary_doc:
        return None

    print(f"Successfully loaded primary document: '{primary_doc.get('title')}'")

    # This will be our final, fully merged document
    merged_document = {
        "documentId": primary_doc.get("documentId"),
        "title": primary_doc.get("title"),
        "author": primary_doc.get("author"),
        "full_content": [
            {
                "section": "Summary",
                "text": primary_doc.get("content_summary", "")
            }
        ]
    }
    
    # 2. Check for and process child document chunks
    child_ids = primary_doc.get("childDocumentChunks", [])
    if not child_ids:
        print("No child documents to merge.")
        return merged_document
        
    print(f"Found {len(child_ids)} child document(s) to resolve.")

    # 3. Fetch each child and append its content
    for child_id in child_ids:
        print(f"  -> Fetching child chunk: {child_id}")
        child_doc = load_document_from_db(child_id)
        if child_doc:
            # 4. Append the child content to our merged document
            merged_document["full_content"].append({
                "section": child_doc.get("section_title", "Untitled Section"),
                "text": child_doc.get("content", "")
            })
            print(f"  -> Merged section: '{child_doc.get('section_title')}'")

    print("--- Merge process complete. ---")
    return merged_document

# --- Main execution ---
if __name__ == "__main__":
    PRIMARY_DOCUMENT_ID = "document289472_primary"
    
    # Run the resolver
    final_document = resolve_and_merge_document(PRIMARY_DOCUMENT_ID)
    
    if final_document:
        print("\n--- Final Merged Document ---")
        # Pretty-print the final JSON object
        print(json.dumps(final_document, indent=2))
