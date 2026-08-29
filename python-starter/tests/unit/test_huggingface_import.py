from rag_service.application.services.huggingface_import import HuggingFaceDatasetImporter


class RecordingIngestion:
    def __init__(self) -> None:
        self.commands = []

    def ingest(self, command) -> int:
        self.commands.append(command)
        return 2


def test_streams_bounded_rows_into_ingestion_service() -> None:
    ingestion = RecordingIngestion()

    def loader(*args, **kwargs):
        assert args == ("owner/game-lore",)
        assert kwargs["streaming"] is True
        return iter([{"title": "Forest", "text": "Ancient trees"}, {"title": "Desert", "text": "Glass dunes"}])

    importer = HuggingFaceDatasetImporter(ingestion, loader=loader)
    rows, chunks = importer.import_rows("owner/game-lore", "train", None, None, ["title", "text"], 1)

    assert (rows, chunks) == (1, 2)
    assert ingestion.commands[0].document_id == "hf:owner/game-lore:train:0"
    assert ingestion.commands[0].content == "title: Forest\n\ntext: Ancient trees"


def test_auto_detects_string_columns_and_skips_empty_rows() -> None:
    ingestion = RecordingIngestion()
    importer = HuggingFaceDatasetImporter(
        ingestion,
        loader=lambda *args, **kwargs: iter([{"score": 4}, {"dialogue": "Welcome, hero", "score": 5}]),
    )

    rows, chunks = importer.import_rows("owner/dialogue", "train", None, None, [], 10)

    assert (rows, chunks) == (1, 2)
    assert ingestion.commands[0].content == "dialogue: Welcome, hero"


def test_falls_back_to_detected_columns_when_requested_column_is_missing() -> None:
    ingestion = RecordingIngestion()
    importer = HuggingFaceDatasetImporter(
        ingestion,
        loader=lambda *args, **kwargs: iter([{"text": "Once upon a tiny world", "score": 5}]),
    )

    rows, chunks = importer.import_rows("roneneldan/TinyStories", "train", None, None, ["YUVA"], 10)

    assert (rows, chunks) == (1, 2)
    assert ingestion.commands[0].content == "text: Once upon a tiny world"
