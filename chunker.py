"""
Part 2: Splitting text into chunks (recursive character splitting + overlap).

After Part 1 we have one huge string of text from a PDF.
We can't search or feed that whole thing to the AI at once, so we
cut it into small, overlapping pieces called "chunks".

Our strategy (recursive character splitting):
  - Try to split on the BIGGEST natural boundary first: paragraphs ("\\n\\n").
  - If a piece is still too big, split it on the next boundary: lines ("\\n").
  - Still too big? Split on spaces (words).
  - Only as a last resort, cut in the middle of a word.

This keeps sentences and paragraphs whole whenever possible.

Then we MERGE the small pieces back together up to a size limit, and
let neighbouring chunks share a little text (overlap) so no idea gets
cut in half at a boundary.
"""


# The separators, ordered from "biggest boundary" to "smallest".
# We deliberately do NOT split on ". " so that periods (and full
# sentences) are never lost — we only break paragraphs, lines, and words.
SEPARATORS = ["\n\n", "\n", " "]


def _recursive_split(text: str, chunk_size: int, separators: list[str]) -> list[str]:
    """
    Phase 1: break `text` into pieces that are each <= chunk_size,
    preferring the biggest natural boundary available.

    Returns a list of small text pieces (paragraphs, lines, or words).
    """
    # Base case: this piece already fits — keep it as is.
    if len(text) <= chunk_size:
        return [text]

    # No separators left to try: hard-cut into fixed-size blocks.
    # (Only happens for something like a giant unbroken string.)
    if not separators:
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    separator = separators[0]        # the boundary we'll try now
    remaining = separators[1:]       # smaller boundaries to try if needed

    pieces = []
    for part in text.split(separator):
        if not part:
            continue  # skip empty strings created by the split
        if len(part) <= chunk_size:
            pieces.append(part)
        else:
            # This part is still too big — recurse with a smaller separator.
            pieces.extend(_recursive_split(part, chunk_size, remaining))
    return pieces


def _overlap_tail(text: str, chunk_overlap: int) -> str:
    """
    Return roughly the last `chunk_overlap` characters of `text`,
    but snapped to start at a word boundary so we don't begin a chunk
    in the middle of a word.
    """
    if chunk_overlap <= 0 or len(text) <= chunk_overlap:
        return text if chunk_overlap > 0 else ""

    tail = text[-chunk_overlap:]
    # Move forward to the first space so the overlap starts on a whole word.
    space = tail.find(" ")
    if space != -1:
        tail = tail[space + 1:]
    return tail


def _merge_with_overlap(pieces: list[str], chunk_size: int, chunk_overlap: int) -> list[str]:
    """
    Phase 2: pack the small pieces into chunks up to `chunk_size`.
    Each new chunk begins with the last `chunk_overlap` characters of the
    previous chunk, so context is never lost at a boundary.
    """
    chunks = []
    current = ""  # the chunk text we're currently building

    for piece in pieces:
        piece = piece.strip()
        if not piece:
            continue

        # What `current` would look like if we added this piece.
        candidate = f"{current} {piece}".strip()

        if current and len(candidate) > chunk_size:
            # Adding the piece would overflow — close the current chunk...
            chunks.append(current)
            # ...and seed the next chunk with the overlap tail.
            overlap = _overlap_tail(current, chunk_overlap)
            current = f"{overlap} {piece}".strip()
        else:
            current = candidate

    # Don't forget the final chunk still being built.
    if current:
        chunks.append(current)

    return chunks


def split_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
    """
    Split a big string into overlapping chunks.

    Args:
        text: the full document text (from read_pdf in Part 1).
        chunk_size: the maximum size of each chunk, in characters.
        chunk_overlap: how many characters neighbouring chunks share.

    Returns:
        A list of chunk strings.
    """
    pieces = _recursive_split(text, chunk_size, SEPARATORS)
    return _merge_with_overlap(pieces, chunk_size, chunk_overlap)


# Run directly to see chunking in action on our sample PDF:
#   python chunker.py
if __name__ == "__main__":
    from pdf_reader import read_pdf

    full_text = read_pdf("documents/sample.pdf")
    chunks = split_text(full_text, chunk_size=300, chunk_overlap=50)

    print(f"Original text length: {len(full_text)} characters")
    print(f"Number of chunks:     {len(chunks)}")
    print("=" * 60)

    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i} ({len(chunk)} chars) ---")
        print(chunk)
