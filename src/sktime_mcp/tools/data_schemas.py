"""Structured config schemas for load_data_source by source type."""

from typing import Any

SCHEMAS = {
    "pandas": {
        "required": ["type", "data", "time_column", "target_column"],
        "optional": [],
        "description": "Load from a pandas-compatible dict with date and value keys.",
        "example": {
            "type": "pandas",
            "data": {"date": ["2020-01", "2020-02"], "value": [100, 200]},
            "time_column": "date",
            "target_column": "value",
        },
    },
    "sql": {
        "required": ["type", "connection_string", "query", "time_column", "target_column"],
        "optional": [],
        "description": "Load from a SQL database using a connection string and query.",
        "example": {
            "type": "sql",
            "connection_string": "postgresql://user:pass@host:5432/db",
            "query": "SELECT date, value FROM sales",
            "time_column": "date",
            "target_column": "value",
        },
    },
    "file": {
        "required": ["type", "path", "time_column", "target_column"],
        "optional": ["sep", "encoding"],
        "description": "Load from a local CSV or supported file path.",
        "example": {
            "type": "file",
            "path": "/path/to/data.csv",
            "time_column": "date",
            "target_column": "value",
        },
    },
    "url": {
        "required": ["type", "url", "time_column", "target_column"],
        "optional": ["sep", "encoding"],
        "description": "Load from a remote URL pointing to a CSV or similar file.",
        "example": {
            "type": "url",
            "url": "https://example.com/data.csv",
            "time_column": "date",
            "target_column": "value",
        },
    },
}


def validate_config(config: dict[str, Any]) -> dict[str, Any]:
    """
    Validate a load_data_source config against its source type schema.

    Returns a dict with:
    - valid: bool
    - missing_fields: list of missing required fields
    - suggestion: example config for the given type
    - error: human-readable error message if invalid
    """
    source_type = config.get("type")

    if not source_type:
        return {
            "valid": False,
            "missing_fields": ["type"],
            "error": "Missing required field 'type'. Must be one of: "
            + ", ".join(SCHEMAS.keys()),
            "suggestion": None,
        }

    if source_type not in SCHEMAS:
        return {
            "valid": False,
            "missing_fields": [],
            "error": f"Unknown source type '{source_type}'. "
            f"Valid types are: {', '.join(SCHEMAS.keys())}",
            "suggestion": None,
        }

    schema = SCHEMAS[source_type]
    missing = [f for f in schema["required"] if f not in config]

    if missing:
        return {
            "valid": False,
            "missing_fields": missing,
            "error": f"Config for type '{source_type}' is missing: {missing}",
            "suggestion": schema["example"],
        }

    return {"valid": True, "missing_fields": [], "error": None, "suggestion": None}