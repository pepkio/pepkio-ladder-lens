"""Integration tests against live Pepkio Tools API."""

from __future__ import annotations

import os

import pytest

from pepkio_ladder_lens.client import PepkioClient

# Local first, then production (param order).
ENVIRONMENTS = [
    ("local", "https://tools.localtest.me"),
    ("production", "https://tools.pepkio.com"),
]


def _api_key_for(base_url: str) -> str | None:
    if "localtest.me" in base_url:
        return os.getenv("LOCAL_PEPKIO_API_KEY")
    return os.getenv("PEPKIO_API_KEY")


@pytest.fixture(params=ENVIRONMENTS, ids=["local", "production"])
def live_client(request):
    env_name, base_url = request.param
    api_key = _api_key_for(base_url)
    if not api_key:
        pytest.skip(f"No API key for {env_name} (set LOCAL_PEPKIO_API_KEY or PEPKIO_API_KEY)")
    with PepkioClient(api_key=api_key, base_url=base_url) as client:
        yield client


def test_get_manifest(live_client: PepkioClient):
    manifest = live_client.get_manifest(refresh=True)
    assert manifest["tool_id"] == "ladder-lens"
    names = live_client.list_examples()
    assert "neb_1kb_single_ladder" in names


def test_run_neb_1kb_single_ladder_example(live_client: PepkioClient):
    inp = live_client.get_example_input("neb_1kb_single_ladder")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.run_id
    assert result.permalink
    assert result.result is not None
    assert isinstance(result.result.get("samples"), list)
    assert isinstance(result.result.get("fit"), dict)
    assert len(result.result["samples"]) == 2
    assert result.result.get("error") is None


def test_run_dual_ladder_smile_example(live_client: PepkioClient):
    inp = live_client.get_example_input("dual_ladder_smile")
    result = live_client.run(inp)
    assert result.status == "completed"
    assert result.result is not None
    assert isinstance(result.result.get("samples"), list)
    assert len(result.result["samples"]) == 1
