"""
Stack Overflow Developer Survey 2025 – Static data client.

The SO survey does not expose a public REST API for results.
This module embeds the official published data from:
  https://survey.stackoverflow.co/2025/technology

Data is organized per-framework with three metric types:
  - usage_pct     : % of respondents who used the framework (All Respondents)
  - admired_pct   : % of past users who want to keep using it
  - desired_pct   : % of non-users who want to learn/use it next year
"""

# ---------------------------------------------------------------------------
# Stack Overflow Developer Survey 2025 – Web Frameworks & Technologies
# Source: https://survey.stackoverflow.co/2025/technology
# Responses: 23,678 (48.3% of total respondents)
# License: Open Database License (ODbL)
# ---------------------------------------------------------------------------

SO_2025_SURVEY_DATA = {
    # ── All 18 tracked frameworks ─────────────────────────────────────
    "Node.js": {
        "usage_pct": 48.7,
        "admired_pct": 52.2,
        "desired_pct": 29.7,
    },
    "React": {
        "usage_pct": 44.7,
        "admired_pct": 52.1,
        "desired_pct": 30.7,
    },
    "Next.js": {
        "usage_pct": 20.8,
        "admired_pct": 45.5,
        "desired_pct": 14.9,
    },
    "Angular": {
        "usage_pct": 18.2,
        "admired_pct": 44.7,
        "desired_pct": 12.6,
    },
    "Vue.js": {
        "usage_pct": 17.6,
        "admired_pct": 50.9,
        "desired_pct": 15.3,
    },
    "Express.js": {
        "usage_pct": 19.9,
        "admired_pct": 45.5,
        "desired_pct": 11.4,
    },
    "FastAPI": {
        "usage_pct": 14.8,
        "admired_pct": 55.5,
        "desired_pct": 13.0,
    },
    "Spring Boot": {
        "usage_pct": 14.7,
        "admired_pct": 53.7,
        "desired_pct": 11.0,
    },
    "ASP.NET Core": {
        "usage_pct": 19.7,
        "admired_pct": 61.3,
        "desired_pct": 14.7,
    },
    "Django": {
        "usage_pct": 12.6,
        "admired_pct": 46.4,
        "desired_pct": 10.4,
    },
    "Flask": {
        "usage_pct": 14.4,
        "admired_pct": 41.7,
        "desired_pct": 8.9,
    },
    "Svelte": {
        "usage_pct": 7.2,
        "admired_pct": 62.4,
        "desired_pct": 11.1,
    },
    "Laravel": {
        "usage_pct": 8.9,
        "admired_pct": 47.8,
        "desired_pct": 6.5,
    },
    "NestJS": {
        "usage_pct": 6.7,
        "admired_pct": 49.8,
        "desired_pct": 6.0,
    },
    "Ruby on Rails": {
        "usage_pct": 5.9,
        "admired_pct": 52.0,
        "desired_pct": 5.5,
    },
    "Astro": {
        "usage_pct": 4.5,
        "admired_pct": 62.2,
        "desired_pct": 5.9,
    },
    "Nuxt": {
        "usage_pct": 4.0,
        "admired_pct": 46.4,
        "desired_pct": 4.0,
    },
    "Phoenix": {
        "usage_pct": 2.4,
        "admired_pct": 79.0,
        "desired_pct": 4.0,
    },
    # ── Additional context frameworks (not tracked, for reference) ───
    "jQuery": {
        "usage_pct": 23.4,
        "admired_pct": 31.4,
        "desired_pct": 9.0,
    },
    "Blazor": {
        "usage_pct": 7.0,
        "admired_pct": 51.9,
        "desired_pct": 7.1,
    },
    "Deno": {
        "usage_pct": 4.0,
        "admired_pct": 52.1,
        "desired_pct": 6.5,
    },
}

# Mapping from our tracked framework names to SO survey keys.
# Frameworks not in the SO survey are omitted (get_metrics returns None).
FRAMEWORK_TO_SO_KEY = {
    "Vue.js": "Vue.js",
    "React": "React",
    "Next.js": "Next.js",
    "Angular": "Angular",
    "Svelte": "Svelte",
    "Nuxt": "Nuxt",
    "Astro": "Astro",
    # Remix: not a separate SO 2025 survey entry
    "FastAPI": "FastAPI",
    "Express.js": "Express.js",
    "Spring Boot": "Spring Boot",
    "Django": "Django",
    "Flask": "Flask",
    "NestJS": "NestJS",
    "Laravel": "Laravel",
    "Ruby on Rails": "Ruby on Rails",
    "Phoenix": "Phoenix",
    "ASP.NET Core": "ASP.NET Core",
}


class StackOverflowClient:
    """Returns Stack Overflow Developer Survey 2025 metrics for tracked frameworks."""

    SURVEY_YEAR = 2025
    SURVEY_URL = "https://survey.stackoverflow.co/2025/technology"
    TOTAL_RESPONSES = 23_678

    def get_metrics(self, framework_name: str) -> dict | None:
        """
        Return {'so_usage_pct', 'so_admired_pct', 'so_desired_pct'} for a framework.
        Returns None if the framework is not in the survey data.
        """
        so_key = FRAMEWORK_TO_SO_KEY.get(framework_name)
        if so_key is None:
            return None

        data = SO_2025_SURVEY_DATA.get(so_key)
        if data is None:
            return None

        return {
            "so_usage_pct": data["usage_pct"],
            "so_admired_pct": data["admired_pct"],
            "so_desired_pct": data["desired_pct"],
        }

    def get_all_tracked(self) -> dict:
        """Return SO metrics for all tracked frameworks as {framework_name: metrics_dict}."""
        results = {}
        for fw_name in FRAMEWORK_TO_SO_KEY:
            metrics = self.get_metrics(fw_name)
            if metrics:
                results[fw_name] = metrics
        return results
