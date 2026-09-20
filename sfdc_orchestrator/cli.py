from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import DeliveryPipeline, load_config


def main() -> None:
    parser = argparse.ArgumentParser(description="Salesforce Delivery Orchestrator")
    parser.add_argument("command", choices=("plan", "run"))
    parser.add_argument("issue_key")
    parser.add_argument("--config", default="config/orchestrator.yaml")
    parser.add_argument("--approve", action="append", default=[])
    args = parser.parse_args()
    config_path = Path(args.config)
    if not config_path.exists():
        config_path = Path("config/orchestrator.example.yaml")
    pipeline = DeliveryPipeline(load_config(config_path))
    result = pipeline.task_contract(args.issue_key) if args.command == "plan" else pipeline.execute(args.issue_key, set(args.approve))
    print(json.dumps(result if isinstance(result, dict) else result.__dict__, indent=2))


if __name__ == "__main__":
    main()
