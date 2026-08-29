from collections.abc import Callable, Iterable, Mapping
from typing import Any

from rag_service.application.dto import IngestCommand
from rag_service.application.services.ingestion import IngestionService

DatasetLoader = Callable[..., Iterable[Mapping[str, Any]]]


def load_huggingface_dataset(*args: Any, **kwargs: Any) -> Iterable[Mapping[str, Any]]:
    from datasets import load_dataset

    return load_dataset(*args, **kwargs)


class HuggingFaceDatasetImporter:
    def __init__(
        self,
        ingestion: IngestionService,
        token: str | None = None,
        loader: DatasetLoader = load_huggingface_dataset,
    ) -> None:
        self._ingestion = ingestion
        self._token = token
        self._loader = loader

    def import_rows(
        self,
        dataset_id: str,
        split: str,
        config_name: str | None,
        revision: str | None,
        text_columns: list[str],
        max_rows: int,
    ) -> tuple[int, int]:
        rows = self._loader(
            dataset_id,
            name=config_name,
            split=split,
            revision=revision,
            streaming=True,
            token=self._token,
        )
        row_count = chunk_count = 0
        for index, row in enumerate(rows):
            if index >= max_rows:
                break
            detected_columns = [key for key, value in row.items() if isinstance(value, str)]
            columns = [column for column in text_columns if column in detected_columns] or detected_columns
            content = "\n\n".join(
                f"{column}: {row[column]}" for column in columns if isinstance(row[column], str) and row[column].strip()
            )
            if not content:
                continue
            document_id = f"hf:{dataset_id}:{split}:{index}"
            metadata = {"source": "huggingface", "dataset_id": dataset_id, "split": split, "row": str(index)}
            chunk_count += self._ingestion.ingest(IngestCommand(document_id, content, metadata))
            row_count += 1
        return row_count, chunk_count
