from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Stage:
    id: str
    requires: tuple[str, ...] = ()
    approval: str | None = None


@dataclass
class Run:
    issue_key: str
    stages: list[str] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)
