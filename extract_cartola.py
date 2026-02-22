"""Backward-compatible entrypoint for facts ingestion."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent / "src"))

from cartola_pipeline.ingestion.extract_facts import main

if __name__ == "__main__":
    main()
