"""
Validation tests for pyproject.toml.

Testing framework: pytest
"""

from __future__ import annotations

import pathlib
import re
import sys
import typing as _t

import pytest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"


def _read_pyproject_text() -> str:
    assert PYPROJECT_PATH.exists(), f"pyproject.toml not found at {PYPROJECT_PATH}"
    return PYPROJECT_PATH.read_text(encoding="utf-8")


def _parse_toml() -> _t.Optional[dict]:
    """
    Parse pyproject.toml using stdlib tomllib when available (Python 3.11+).

    Returns dict on success, or None if tomllib is unavailable (tests using it will skip).
    """
    if sys.version_info < (3, 11):
        return None
    try:
        import tomllib  # type: ignore
    except ImportError:
        return None
    try:
        return tomllib.loads(_read_pyproject_text())
    except tomllib.TOMLDecodeError as e:
        # On supported Python, parsing should succeed for valid TOML
        pytest.fail(f"tomllib failed to parse pyproject.toml: {e}")


def test_pyproject_exists_and_nonempty():
    assert PYPROJECT_PATH.exists(), "pyproject.toml should exist at repository root"
    text = _read_pyproject_text()
    assert text.strip(), "pyproject.toml should not be empty"
    assert "[project]" in text, "Missing [project] section"
    assert "[build-system]" in text, "Missing [build-system] section"


def test_project_core_metadata_matches_diff_textually():
    text = _read_pyproject_text()
    assert re.search(r'(?m)^\s*name\s*=\s*"vocalizr"\s*$', text), (
        "Expected project name 'vocalizr'"
    )
    assert re.search(r'(?m)^\s*version\s*=\s*"0\.0\.1"\s*$', text), (
        "Expected version '0.0.1'"
    )
    assert re.search(r'(?m)^\s*readme\s*=\s*"README\.md"\s*$', text), (
        "Expected readme 'README.md'"
    )
    assert re.search(r'(?m)^\s*description\s*=\s*".+?"\s*$', text), (
        "Description should be non-empty"
    )
    assert re.search(r'(?m)^\s*requires-python\s*=\s*">=3\.12,\s*<3\.14"\s*$', text), (
        "Expected requires-python '>=3.12, <3.14'"
    )


def test_project_authors_contains_expected_person():
    text = _read_pyproject_text()
    assert re.search(
        r'\{\s*name\s*=\s*"Mohamed Hisham Abdelzaher"\s*,\s*email\s*=\s*"mohamed\.hisham\.abdelzaher@gmail\.com"\s*\}',
        text,
    ), "Expected author 'Mohamed Hisham Abdelzaher' with specified email"


@pytest.mark.parametrize(
    "pattern",
    [
        r'"gradio\[mcp\]>=5\.38\.0"',
        r'"kokoro>=0\.9\.4"',
        r'"soundfile>=0\.13\.1"',
        r'"pip>=25\.1\.1"',
    ],
)
def test_project_dependencies_include_expected_entries(pattern: str):
    text = _read_pyproject_text()
    assert re.search(pattern, text), (
        f"Dependency {pattern} not found in [project].dependencies"
    )


def test_project_scripts_entry_point_is_correct():
    text = _read_pyproject_text()
    assert "[project.scripts]" in text, "Missing [project.scripts] section"
    assert re.search(r'(?m)^\s*vocalizr\s*=\s*"vocalizr\.__main__:main"\s*$', text), (
        "Expected script entry: vocalizr = 'vocalizr.__main__:main'"
    )


def test_project_urls_repository_and_issues():
    text = _read_pyproject_text()
    assert "[project.urls]" in text, "Missing [project.urls] section"
    assert re.search(
        r'(?m)^\s*Repository\s*=\s*"https://github\.com/AlphaSphereDotAI/vocalizr\.git"\s*$',
        text,
    ), "Repository URL must point to the .git repo"
    assert re.search(
        r'(?m)^\s*Issues\s*=\s*"https://github\.com/AlphaSphereDotAI/vocalizr/issues"\s*$',
        text,
    ), "Issues URL must point to the GitHub issues page"


def test_project_urls_homepage_and_docs_are_commented_or_absent():
    text = _read_pyproject_text()
    # Ensure there are no active (uncommented) Homepage/Documentation keys per diff
    assert not re.search(r"(?m)^\s*Homepage\s*=", text), (
        "Homepage should be commented out or absent"
    )
    assert not re.search(r"(?m)^\s*Documentation\s*=", text), (
        "Documentation should be commented out or absent"
    )


def test_build_system_uses_uv_build():
    text = _read_pyproject_text()
    assert re.search(r'(?m)^\s*requires\s*=\s*\[\s*"uv_build"\s*\]\s*$', text), (
        "build-system.requires should be ['uv_build']"
    )
    assert re.search(r'(?m)^\s*build-backend\s*=\s*"uv_build"\s*$', text), (
        "build-backend should be 'uv_build'"
    )


@pytest.mark.parametrize(
    "dev_dep_pattern",
    [
        r'"pytest-emoji>=0\.2\.0"',
        r'"pytest-md>=0\.2\.0"',
        r'"pytest-mergify>=2025\.9\.10\.1"',
        r'"ruff>=0\.13\.1"',
        r'"ty>=0\.0\.1a20"',
    ],
)
def test_dependency_groups_dev_contains_expected_tools(dev_dep_pattern: str):
    text = _read_pyproject_text()
    assert "[dependency-groups]" in text, "Missing [dependency-groups] section"
    assert re.search(dev_dep_pattern, text), (
        f"Dev dependency {dev_dep_pattern} not found under [dependency-groups].dev"
    )


def test_uv_index_and_sources_configuration_matches_diff():
    text = _read_pyproject_text()
    assert "[[tool.uv.index]]" in text, "Missing [[tool.uv.index]] array-of-tables"
    assert re.search(r'(?m)^\s*name\s*=\s*"pytorch-cu124"\s*$', text), (
        "uv.index name should be 'pytorch-cu124'"
    )
    assert re.search(
        r'(?m)^\s*url\s*=\s*"https://download\.pytorch\.org/whl/cu124"\s*$', text
    ), "uv.index url should be the CUDA 12.4 wheel index"
    assert re.search(r"(?m)^\s*explicit\s*=\s*true\s*$", text), (
        "uv.index explicit must be true"
    )
    assert "[tool.uv.sources]" in text, "Missing [tool.uv.sources] table"
    assert re.search(
        r'(?m)^\s*torch\s*=\s*\{\s*index\s*=\s*"pytorch-cu124"\s*\}\s*$', text
    ), "tool.uv.sources must map torch to index 'pytorch-cu124'"


def test_parsed_toml_keypaths_and_values_if_supported():
    data = _parse_toml()
    if data is None:
        pytest.skip("tomllib unavailable; skipping parsed-TOML checks")

    project = data.get("project") or {}
    assert project.get("name") == "vocalizr"
    assert project.get("version") == "0.0.1"
    assert project.get("readme") == "README.md"
    assert project.get("requires-python") == ">=3.12, <3.14"

    deps = project.get("dependencies") or []
    for expected in [
        "gradio[mcp]>=5.38.0",
        "kokoro>=0.9.4",
        "soundfile>=0.13.1",
        "pip>=25.1.1",
    ]:
        assert expected in deps

    scripts = project.get("scripts") or {}
    assert scripts.get("vocalizr") == "vocalizr.__main__:main"

    urls = project.get("urls") or {}
    assert urls.get("Repository") == "https://github.com/AlphaSphereDotAI/vocalizr.git"
    assert urls.get("Issues") == "https://github.com/AlphaSphereDotAI/vocalizr/issues"

    build_system = data.get("build-system") or {}
    assert build_system.get("requires") == ["uv_build"]
    assert build_system.get("build-backend") == "uv_build"

    dg = data.get("dependency-groups") or {}
    dev = dg.get("dev") or []
    for expected in [
        "pytest-emoji>=0.2.0",
        "pytest-md>=0.2.0",
        "pytest-mergify>=2025.9.10.1",
        "ruff>=0.13.1",
        "ty>=0.0.1a20",
    ]:
        assert expected in dev

    tool = data.get("tool") or {}
    uv = tool.get("uv") or {}
    indexes = uv.get("index") or []
    assert any(
        i.get("name") == "pytorch-cu124"
        and i.get("url") == "https://download.pytorch.org/whl/cu124"
        and i.get("explicit") is True
        for i in indexes
    ), "Expected pytorch-cu124 index entry"
    sources = uv.get("sources") or {}
    assert sources.get("torch", {}).get("index") == "pytorch-cu124"
