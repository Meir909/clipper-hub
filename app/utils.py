from __future__ import annotations

from datetime import datetime

from flask import Flask


def register_template_utils(app: Flask) -> None:
    def euro(value_cents: int | None) -> str:
        value = value_cents or 0
        formatted = f"€{value / 100:,.2f}"
        return formatted.replace(",", " ")  # thin space for thousands

    def status_class(status: str) -> str:
        mapping = {
            "pending": "badge-soft-warning",
            "approved": "badge-soft-success",
            "rejected": "badge-soft-danger",
            "paid": "badge-soft-success",
        }
        return mapping.get(status.lower(), "badge-soft-muted")

    app.jinja_env.filters["euro"] = euro
    app.jinja_env.filters["status_class"] = status_class

    @app.context_processor
    def inject_globals() -> dict[str, int]:
        return {"current_year": datetime.utcnow().year}
