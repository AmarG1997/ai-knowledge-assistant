"""
Part 1: Reading a PDF into plain text.

This is the very first step of our AI Knowledge Assistant.
Before we can search or answer questions about a document,
we need to pull the raw text out of the PDF file.

We use the `pypdf` library, which opens a PDF and lets us
read it page by page.
"""

from pypdf import PdfReader


def read_pdf(file_path: str) -> str:
    """
    Open a PDF file and return all of its text as one big string.

    Args:
        file_path: path to the .pdf file (e.g. "documents/python.pdf")

    Returns:
        A single string containing the text of every page.
    """
    # PdfReader opens the file and understands the PDF format for us.
    reader = PdfReader(file_path)

    # We'll collect the text from each page into this list.
    all_pages_text = []

    # A PDF is a list of pages. We loop through them one by one.
    # `enumerate` gives us the page number too (starting at 0).
    for page_number, page in enumerate(reader.pages):
        # extract_text() reads the words off a single page.
        text = page.extract_text()

        # Some pages (like image-only pages) may have no text.
        # We skip those so we don't add empty gaps.
        if text:
            all_pages_text.append(text)

    # Join every page's text together, separated by a blank line.
    return "\n\n".join(all_pages_text)


# This block only runs when you execute this file directly:
#   python pdf_reader.py documents/python.pdf
# It does NOT run when another file imports read_pdf().
if __name__ == "__main__":
    import sys

    # Read the file path from the command line, or use a default.
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "documents/sample.pdf"

    print(f"Reading: {path}\n")
    content = read_pdf(path)

    # Show a quick summary so we can confirm it worked.
    print(f"Total characters extracted: {len(content)}")
    print("\n----- First 500 characters -----\n")
    print(content[:500])
