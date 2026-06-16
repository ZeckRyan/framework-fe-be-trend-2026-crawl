"""
Main pipeline orchestrator.
Calls GitHub, NPM, PyPI, and/or Stack Overflow APIs for each target framework
and writes raw results to data/raw/raw_framework_data.json.

Usage examples:
  python -m scraper.main_pipeline                          # all sources (default)
  python -m scraper.main_pipeline --sources github,npm,pypi
  python -m scraper.main_pipeline --sources stackoverflow
  python -m scraper.main_pipeline --sources github,stackoverflow
"""

import json
import os
import time
from datetime import datetime, timezone

from scraper.api_clients import (
    FRAMEWORK_REGISTRY,
    GitHubClient,
    NPMClient,
    PyPIClient,
)
from scraper.stackoverflow_client import StackOverflowClient

# Resolve project root (parent of /scraper)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
RAW_OUTPUT_FILE = os.path.join(RAW_DATA_DIR, "raw_framework_data.json")

# All available data sources
ALL_SOURCES = {"github", "npm", "pypi", "stackoverflow"}


def parse_sources(sources_arg: str) -> set[str]:
    """Parse comma-separated source string into a set of source names."""
    if sources_arg.strip().lower() == "all":
        return ALL_SOURCES.copy()
    requested = {s.strip().lower() for s in sources_arg.split(",") if s.strip()}
    invalid = requested - ALL_SOURCES
    if invalid:
        print(f"[Pipeline] WARNING: Unknown sources ignored: {invalid}")
        print(f"[Pipeline] Valid sources: {ALL_SOURCES}")
    return requested & ALL_SOURCES


def run_pipeline(
    github_token: str | None = None,
    sources: set[str] | None = None,
) -> dict:
    """
    Execute the crawling pipeline for selected data sources.

    Args:
        github_token: Optional GitHub PAT for higher rate limits.
        sources: Set of source names to use. Defaults to ALL_SOURCES.

    Returns:
        The aggregated result dict (also written to disk).
    """
    if sources is None:
        sources = ALL_SOURCES.copy()

    print(f"[Pipeline] Active sources: {sorted(sources)}")
    print(f"[Pipeline] Target frameworks: {list(FRAMEWORK_REGISTRY.keys())}")
    print()

    # Initialize clients for selected sources
    github = GitHubClient(token=github_token) if "github" in sources else None
    npm = NPMClient() if "npm" in sources else None
    pypi = PyPIClient() if "pypi" in sources else None
    stackoverflow = StackOverflowClient() if "stackoverflow" in sources else None

    results = {}

    for framework_name, meta in FRAMEWORK_REGISTRY.items():
        print(f"[Pipeline] Fetching data for {framework_name}...")

        entry = {
            "category": meta["category"],
            "github_repo": meta["github_repo"],
        }

        # --- GitHub metrics ---
        if github and meta["github_repo"]:
            gh_metrics = github.get_metrics(meta["github_repo"])
            entry.update(gh_metrics)
            time.sleep(1)  # Respect rate limits
        else:
            entry.update({"stargazers_count": 0, "forks_count": 0, "open_issues_count": 0})

        # --- NPM weekly downloads ---
        if npm and meta["npm_package"]:
            entry["npm_weekly_downloads"] = npm.get_weekly_downloads(meta["npm_package"])
        else:
            entry["npm_weekly_downloads"] = 0

        # --- PyPI weekly downloads ---
        if pypi and meta["pypi_package"]:
            entry["pypi_weekly_downloads"] = pypi.get_weekly_downloads(meta["pypi_package"])
        else:
            entry["pypi_weekly_downloads"] = 0

        entry["total_weekly_downloads"] = (
            entry["npm_weekly_downloads"] + entry["pypi_weekly_downloads"]
        )

        # --- Stack Overflow survey metrics ---
        if stackoverflow:
            so_metrics = stackoverflow.get_metrics(framework_name)
            if so_metrics:
                entry.update(so_metrics)
            else:
                entry.update({"so_usage_pct": 0.0, "so_admired_pct": 0.0, "so_desired_pct": 0.0})
        else:
            entry.update({"so_usage_pct": 0.0, "so_admired_pct": 0.0, "so_desired_pct": 0.0})

        results[framework_name] = entry

    # Wrap with metadata
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sources_used": sorted(sources),
        "frameworks": results,
    }

    # Ensure output directory exists
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    # Write to disk
    with open(RAW_OUTPUT_FILE, "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=2, ensure_ascii=False)

    print(f"\n[Pipeline] Raw data written to {RAW_OUTPUT_FILE}")
    print(f"[Pipeline] Sources used: {sorted(sources)}")
    return output


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Framework Trends – Data Crawling Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                  # All sources (default)
  %(prog)s --sources github,npm,pypi         # Crawl only (no surveys)
  %(prog)s --sources stackoverflow           # Stack Overflow survey only
  %(prog)s --sources github,stackoverflow    # GitHub + Stack Overflow combined
        """,
    )
    parser.add_argument(
        "--sources",
        default="all",
        help=(
            "Comma-separated list of data sources to use. "
            "Options: github, npm, pypi, stackoverflow, all. "
            "Default: all"
        ),
    )
    parser.add_argument(
        "--github-token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="Optional GitHub personal access token (or set GITHUB_TOKEN env var)",
    )
    args = parser.parse_args()

    active_sources = parse_sources(args.sources)
    if not active_sources:
        print("[Pipeline] ERROR: No valid sources selected. Exiting.")
        exit(1)

    run_pipeline(github_token=args.github_token, sources=active_sources)
