from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExtractionResult:
    text: str
    warnings: list[str] = field(default_factory=list)
    meta: dict[str, Any] = field(default_factory=dict)
