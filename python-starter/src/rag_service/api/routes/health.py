from fastapi import APIRouter

router = APIRouter(tags=["operations"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
