from sfdc_orchestrator.pipeline import DeliveryPipeline, branch_name


def config():
    return {"project": {"branch_pattern": "feature/{issue_key}-{slug}"}, "safety": {"dry_run": True},
            "pipeline": {"stages": [{"id": "plan", "requires": [], "approval": "plan"}, {"id": "build", "requires": ["plan"]}]}}


def test_gate_stops_pipeline(tmp_path):
    run = DeliveryPipeline(config(), tmp_path).execute("ABC-1", set())
    assert run.stages == []
    assert run.evidence["plan"]["status"] == "awaiting_approval"


def test_approved_pipeline_runs(tmp_path):
    run = DeliveryPipeline(config(), tmp_path).execute("ABC-1", {"plan"})
    assert run.stages == ["plan", "build"]


def test_branch_name_is_safe():
    assert branch_name(config(), "ABC-1", "Add Account: Owner Lookup!") == "feature/abc-1-add-account-owner-lookup"
