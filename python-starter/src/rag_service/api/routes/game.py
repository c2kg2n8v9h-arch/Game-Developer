from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(include_in_schema=False)
_GAME_HTML = Path(__file__).resolve().parents[2] / "web" / "game.html"


@router.get("/", response_class=RedirectResponse)
def game_redirect() -> RedirectResponse:
    return RedirectResponse("/game")


@router.get("/game", response_class=HTMLResponse)
def game() -> HTMLResponse:
    return HTMLResponse(_GAME_HTML.read_text(encoding="utf-8"))
