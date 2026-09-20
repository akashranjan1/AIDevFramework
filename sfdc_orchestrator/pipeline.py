from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import re
import uuid

import yaml

from .models import Run, Stage


class PipelineError(RuntimeError):
    pass


def load_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as stream:
        return yaml.safe_load(stream)


def stages(config: dict[str, Any]) -> list[Stage]:
    return [Stage(item["id"], tuple(item.get("requires", [])), item.get("approval"))
            for item in config["pipeline"]["stages"]]


def branch_name(config: dict[str, Any], issue_key: str, summary: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", summary.lower()).strip("-")[:50]
    return config["project"]["branch_pattern"].format(issue_key=issue_key.lower(), slug=slug)


class DeliveryPipeline:
    def __init__(self, config: dict[str, Any], root: Path = Path(".")):
        self.config, self.root = config, root

    def task_contract(self, issue_key: str) -> dict[str, Any]:
        return {
            "issue_key": issue_key,
            "skills": ["skills/story-to-plan.md", "skills/salesforce-development.md", "skills/release-validation.md"],
            "guardrails": ["Do not deploy or open a PR without matching approval.", "Return evidence for every test and validation."],
            "result_schema": "schemas/agent-result.schema.json",
        }

    def execute(self, issue_key: str, approvals: set[str]) -> Run:
        run, completed = Run(issue_key=issue_key), set()
        for stage in stages(self.config):
            missing = set(stage.requires) - completed
            if missing:
                raise PipelineError(f"{stage.id} is missing dependencies: {sorted(missing)}")
            if stage.approval and stage.approval not in approvals:
                run.evidence[stage.id] = {"status": "awaiting_approval", "approval": stage.approval}
                break
            run.stages.append(stage.id)
            completed.add(stage.id)
            run.evidence[stage.id] = {"status": "planned" if self.config["safety"]["dry_run"] else "executed"}
        self._write_record(run)
        return run

    def _write_record(self, run: Run) -> None:
        output = self.root / ".delivery-runs"
        output.mkdir(exist_ok=True)
        path = output / f"{run.issue_key}-{uuid.uuid4().hex[:8]}.json"
        path.write_text(json.dumps({"issue_key": run.issue_key, "stages": run.stages, "evidence": run.evidence}, indent=2), encoding="utf-8")
