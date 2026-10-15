from pathlib import Path
import json


class MetadataFilter:

    def __init__(self, chunks_file):
        self.chunks_file = Path(chunks_file)

        if not self.chunks_file.exists():
            raise FileNotFoundError(
                f"Chunks file not found: {self.chunks_file}"
            )

        self.chunks = self._load_chunks()

        print(
            f"Loaded {len(self.chunks)} chunks."
        )

    # ============================================================
    # Load chunks
    # ============================================================

    def _load_chunks(self):

        with open(
            self.chunks_file,
            "r",
            encoding="utf-8"
        ) as f:

            chunks = json.load(f)

        return chunks

    # ============================================================
    # Get chunk by ID
    # ============================================================

    def get_chunk(self, chunk_id):

        if chunk_id < 0 or chunk_id >= len(self.chunks):
            return None

        return self.chunks[chunk_id]

    # ============================================================
    # Enrich FAISS results
    # ============================================================

    def enrich_results(self, results):

       enriched_results = []

       for result in results:

           chunk_id = result["chunk_id"]

           chunk = self.get_chunk(chunk_id)

           if chunk is None:
               continue

           # IMPORTANT:
           # Keep ALL existing hybrid fields
           enriched = result.copy()

           # Add chunk information
           enriched["text"] = chunk.get("text", "")
           enriched["metadata"] = chunk.get("metadata", {})

           enriched_results.append(enriched)

       return enriched_results