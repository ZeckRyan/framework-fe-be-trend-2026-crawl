"""
API clients for GitHub, NPM, and PyPI.
Each client wraps a REST API and returns normalized metric dicts.
"""

import requests


# ---------------------------------------------------------------------------
# Framework registry – maps each target framework to its package identifiers
# ---------------------------------------------------------------------------

FRAMEWORK_REGISTRY = {
    # ── Frontend (8) ──────────────────────────────────────────────────
    "Vue.js": {
        "github_repo": "vuejs/core",
        "npm_package": "vue",
        "pypi_package": None,
        "category": "Frontend",
    },
    "React": {
        "github_repo": "facebook/react",
        "npm_package": "react",
        "pypi_package": None,
        "category": "Frontend",
    },
    "Next.js": {
        "github_repo": "vercel/next.js",
        "npm_package": "next",
        "pypi_package": None,
        "category": "Frontend",
    },
    "Angular": {
        "github_repo": "angular/angular",
        "npm_package": "@angular/core",
        "pypi_package": None,
        "category": "Frontend",
    },
    "Svelte": {
        "github_repo": "sveltejs/svelte",
        "npm_package": "svelte",
        "pypi_package": None,
        "category": "Frontend",
    },
    "Nuxt": {
        "github_repo": "nuxt/nuxt",
        "npm_package": "nuxt",
        "pypi_package": None,
        "category": "Frontend",
    },
    "Astro": {
        "github_repo": "withastro/astro",
        "npm_package": "astro",
        "pypi_package": None,
        "category": "Frontend",
    },
    "Remix": {
        "github_repo": "remix-run/remix",
        "npm_package": "@remix-run/react",
        "pypi_package": None,
        "category": "Frontend",
    },
    # ── Backend (10) ─────────────────────────────────────────────────
    "FastAPI": {
        "github_repo": "fastapi/fastapi",
        "npm_package": None,
        "pypi_package": "fastapi",
        "category": "Backend",
    },
    "Express.js": {
        "github_repo": "expressjs/express",
        "npm_package": "express",
        "pypi_package": None,
        "category": "Backend",
    },
    "Spring Boot": {
        "github_repo": "spring-projects/spring-boot",
        "npm_package": None,
        "pypi_package": None,
        "category": "Backend",
    },
    "Django": {
        "github_repo": "django/django",
        "npm_package": None,
        "pypi_package": "django",
        "category": "Backend",
    },
    "Flask": {
        "github_repo": "pallets/flask",
        "npm_package": None,
        "pypi_package": "flask",
        "category": "Backend",
    },
    "NestJS": {
        "github_repo": "nestjs/nest",
        "npm_package": "@nestjs/core",
        "pypi_package": None,
        "category": "Backend",
    },
    "Laravel": {
        "github_repo": "laravel/laravel",
        "npm_package": None,
        "pypi_package": None,
        "category": "Backend",
    },
    "Ruby on Rails": {
        "github_repo": "rails/rails",
        "npm_package": None,
        "pypi_package": None,
        "category": "Backend",
    },
    "Phoenix": {
        "github_repo": "phoenixframework/phoenix",
        "npm_package": None,
        "pypi_package": None,
        "category": "Backend",
    },
    "ASP.NET Core": {
        "github_repo": "dotnet/aspnetcore",
        "npm_package": None,
        "pypi_package": None,
        "category": "Backend",
    },
}


# ---------------------------------------------------------------------------
# GitHub REST API client
# ---------------------------------------------------------------------------

class GitHubClient:
    """Fetches stargazers, forks, and open issues from GitHub REST API."""

    BASE_URL = "https://api.github.com/repos"

    def __init__(self, token: str | None = None):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github+json",
            "User-Agent": "FrameworkTrendsTracker/1.0",
        })
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def get_metrics(self, repo: str) -> dict:
        """Return {'stargazers_count': int, 'forks_count': int, 'open_issues_count': int}."""
        try:
            response = self.session.get(f"{self.BASE_URL}/{repo}", timeout=15)
            response.raise_for_status()
            data = response.json()
            return {
                "stargazers_count": data.get("stargazers_count", 0),
                "forks_count": data.get("forks_count", 0),
                "open_issues_count": data.get("open_issues_count", 0),
            }
        except requests.RequestException as exc:
            print(f"[GitHubClient] Error fetching {repo}: {exc}")
            return {"stargazers_count": 0, "forks_count": 0, "open_issues_count": 0}


# ---------------------------------------------------------------------------
# NPM Registry API client
# ---------------------------------------------------------------------------

class NPMClient:
    """Fetches weekly download counts from the NPM Registry API."""

    BASE_URL = "https://api.npmjs.org/downloads/point/last-week"

    def get_weekly_downloads(self, package: str) -> int:
        try:
            response = requests.get(
                f"{self.BASE_URL}/{package}",
                headers={"User-Agent": "FrameworkTrendsTracker/1.0"},
                timeout=15,
            )
            response.raise_for_status()
            return response.json().get("downloads", 0)
        except requests.RequestException as exc:
            print(f"[NPMClient] Error fetching {package}: {exc}")
            return 0


# ---------------------------------------------------------------------------
# PyPI Stats API client
# ---------------------------------------------------------------------------

class PyPIClient:
    """Fetches weekly download counts from the PyPI Stats API."""

    BASE_URL = "https://pypistats.org/api/packages"

    def get_weekly_downloads(self, package: str) -> int:
        try:
            response = requests.get(
                f"{self.BASE_URL}/{package}/recent",
                headers={"User-Agent": "FrameworkTrendsTracker/1.0"},
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            # 'data' contains 'last_week' key with download count
            return data.get("data", {}).get("last_week", 0)
        except requests.RequestException as exc:
            print(f"[PyPIClient] Error fetching {package}: {exc}")
            return 0
