"""
Data processor: reads raw_framework_data.json, normalizes metrics,
computes Market_Dominance_Score (source-aware), injects static metadata,
and exports processed CSV + JSON.

Scoring adapts based on which data sources were used in the pipeline:
  - GitHub + NPM/PyPI only:   Score = stars * 0.4 + downloads * 0.6
  - Stack Overflow only:      Score = so_usage * 0.5 + so_admired * 0.25 + so_desired * 0.25
  - All sources combined:     Score = stars * 0.2 + downloads * 0.3 + so_usage * 0.25
                                     + so_admired * 0.125 + so_desired * 0.125
"""

import json
import os

import pandas as pd

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAW_INPUT = os.path.join(PROJECT_ROOT, "data", "raw", "raw_framework_data.json")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
CSV_OUTPUT = os.path.join(PROCESSED_DIR, "processed_framework_data.csv")
JSON_OUTPUT = os.path.join(PROCESSED_DIR, "processed_framework_data.json")


# ---------------------------------------------------------------------------
# Static metadata injection
# ---------------------------------------------------------------------------

STATIC_METADATA = {
    # ── Frontend (8) ──────────────────────────────────────────────────
    "Vue.js": {
        "audience_label": "Terbaik untuk MVP & Tim Kecil",
        "pros": ["Kurva belajar rendah", "SFC Flow intuitif", "Dokumentasi lengkap"],
        "cons": ["Ekosistem enterprise kecil", "Plugin terbatas", "Komunitas lebih kecil dari React"],
    },
    "React": {
        "audience_label": "Ekosistem Terbesar & Paling Fleksibel",
        "pros": ["Komunitas sangat besar", "Ekosistem luas", "Fleksibilitas tinggi"],
        "cons": ["Kurva belajar menengah", "Boilerplate banyak", "Fragmentasi library"],
    },
    "Next.js": {
        "audience_label": "Standar Skala Enterprise",
        "pros": ["Performa SSR", "Optimasi Otomatis", "Full-stack framework"],
        "cons": ["Kompleksitas server", "Vendor lock-in Vercel", "Bundle size besar"],
    },
    "Angular": {
        "audience_label": "Solusi Enterprise Terstruktur",
        "pros": ["Opinionated framework", "Built-in tooling", "TypeScript native"],
        "cons": ["Kurva belajar tinggi", "Bundle besar", "Verbosity tinggi"],
    },
    "Svelte": {
        "audience_label": "Compiler-first, Performa Maksimal",
        "pros": ["Tanpa virtual DOM", "Bundle paling ringan", "Sintaks sederhana"],
        "cons": ["Ekosistem masih muda", "Dukungan enterprise terbatas", "Komunitas kecil"],
    },
    "Nuxt": {
        "audience_label": "Vue Full-stack Meta-framework",
        "pros": ["SSR/SSG bawaan", "Auto-import", "Modular architecture"],
        "cons": ["Tergantung ekosistem Vue", "Kompleksitas konfigurasi", "Komunitas lebih kecil dari Next.js"],
    },
    "Astro": {
        "audience_label": "Content-first, Island Architecture",
        "pros": ["Zero JS by default", "Multi-framework support", "Performa halaman statis terbaik"],
        "cons": ["Tidak cocok untuk SPA", "Ekosistem plugin terbatas", "Masih relatif baru"],
    },
    "Remix": {
        "audience_label": "Web Standards-first, Progressive Enhancement",
        "pros": ["Nested routing", "Built-in data loading", "Progressive enhancement"],
        "cons": ["Adopsi masih kecil", "Kurva belajar unik", "Dokumentasi terbatas"],
    },
    # ── Backend (10) ─────────────────────────────────────────────────
    "FastAPI": {
        "audience_label": "Pilihan Utama AI & Data",
        "pros": ["Eksekusi asinkron", "Validasi otomatis", "Dokumentasi OpenAPI"],
        "cons": ["Plugin spesifik terbatas", "Ekosistem muda", "ORM belum matang"],
    },
    "Express.js": {
        "audience_label": "Backend JS Ringan & Minimalis",
        "pros": ["Minimalis & ringan", "Ekosistem middleware luas", "Kurva belajar rendah"],
        "cons": ["Tidak ada arsitektur bawaan", "Rawan callback hell", "Manajemen error manual"],
    },
    "Spring Boot": {
        "audience_label": "Enterprise Java Teruji",
        "pros": ["Stabil & teruji", "Ekosistem enterprise", "Microservices ready"],
        "cons": ["Memory footprint besar", "Konfigurasi kompleks", "Startup lambat"],
    },
    "Django": {
        "audience_label": "Full-stack Python Matang",
        "pros": ["Batteries-included", "Admin panel bawaan", "ORM matang"],
        "cons": ["Monolitik", "Kurang cocok microservice", "Performa lebih lambat"],
    },
    "Flask": {
        "audience_label": "Microframework Python Ringan",
        "pros": ["Sangat ringan", "Fleksibel", "Mudah dipelajari"],
        "cons": ["Tidak ada ORM bawaan", "Arsitektur manual", "Tidak cocok aplikasi besar tanpa plugin"],
    },
    "NestJS": {
        "audience_label": "Enterprise TypeScript Terstruktur",
        "pros": ["Arsitektur modular", "TypeScript-first", "Dukungan microservices"],
        "cons": ["Kompleksitas tinggi", "Kurva belajar curam", "Overhead untuk proyek kecil"],
    },
    "Laravel": {
        "audience_label": "Full-stack PHP Elegan",
        "pros": ["Sintaks elegan", "Eloquent ORM", "Ekosistem luas (Forge, Vapor)"],
        "cons": ["Performa lebih lambat", "Ketergantungan PHP", "Tidak cocok real-time tanpa tooling tambahan"],
    },
    "Ruby on Rails": {
        "audience_label": "Rapid Prototyping Legend",
        "pros": ["Convention over configuration", "Gem ecosystem kaya", "Developer happiness"],
        "cons": ["Performa lebih lambat", "Adopsi menurun", "Kurva belajar Ruby"],
    },
    "Phoenix": {
        "audience_label": "Real-time Elixir Powerhouse",
        "pros": ["Fault-tolerant (BEAM VM)", "Real-time bawaan", "Skalabilitas tinggi"],
        "cons": ["Komunitas sangat kecil", "Kurva belajar Elixir", "Lowongan kerja sedikit"],
    },
    "ASP.NET Core": {
        "audience_label": "Enterprise Microsoft Ecosystem",
        "pros": ["Performa tinggi (Kestrel)", "Cross-platform", "Integrasi Azure"],
        "cons": ["Vendor lock-in Microsoft", "Kompleksitas enterprise", "C# ecosystem requirement"],
    },
}


# ---------------------------------------------------------------------------
# Processing functions
# ---------------------------------------------------------------------------

def load_raw_data(path: str = RAW_INPUT) -> tuple[pd.DataFrame, list[str]]:
    """Load raw JSON, flatten into a DataFrame, and return (df, sources_used)."""
    with open(path, encoding="utf-8") as fh:
        raw = json.load(fh)

    sources_used = raw.get("sources_used", ["github", "npm", "pypi"])

    rows = []
    for name, metrics in raw["frameworks"].items():
        rows.append({"framework": name, **metrics})

    return pd.DataFrame(rows), sources_used


def _min_max_normalize(series: pd.Series) -> pd.Series:
    """Apply min-max normalization to a pandas Series."""
    s_min, s_max = series.min(), series.max()
    if s_max - s_min == 0:
        return pd.Series(0.0, index=series.index)
    return (series - s_min) / (s_max - s_min)


def normalize_and_score(df: pd.DataFrame, sources_used: list[str]) -> pd.DataFrame:
    """
    Apply min-max normalization and compute Market_Dominance_Score.
    Scoring formula adapts based on which data sources are available.
    """
    df = df.copy()
    has_crawl = "github" in sources_used or "npm" in sources_used or "pypi" in sources_used
    has_so = "stackoverflow" in sources_used

    # --- Normalize crawl metrics ---
    if has_crawl:
        df["norm_stargazers_count"] = _min_max_normalize(df["stargazers_count"])
        df["norm_total_weekly_downloads"] = _min_max_normalize(df["total_weekly_downloads"])

    # --- Normalize Stack Overflow metrics ---
    if has_so:
        df["norm_so_usage"] = _min_max_normalize(df.get("so_usage_pct", pd.Series(0.0)))
        df["norm_so_admired"] = _min_max_normalize(df.get("so_admired_pct", pd.Series(0.0)))
        df["norm_so_desired"] = _min_max_normalize(df.get("so_desired_pct", pd.Series(0.0)))

    # --- Compute composite score based on available sources ---
    if has_crawl and has_so:
        # ALL sources: balanced blend of crawl + survey
        df["Market_Dominance_Score"] = (
            df["norm_stargazers_count"] * 0.20
            + df["norm_total_weekly_downloads"] * 0.30
            + df["norm_so_usage"] * 0.25
            + df["norm_so_admired"] * 0.125
            + df["norm_so_desired"] * 0.125
        )
        print("[Processor] Scoring: ALL sources (crawl 50% + survey 50%)")

    elif has_crawl:
        # Crawl only: stars + downloads
        df["Market_Dominance_Score"] = (
            df["norm_stargazers_count"] * 0.40
            + df["norm_total_weekly_downloads"] * 0.60
        )
        print("[Processor] Scoring: Crawl only (stars 40% + downloads 60%)")

    elif has_so:
        # Survey only: usage + admired + desired
        df["Market_Dominance_Score"] = (
            df["norm_so_usage"] * 0.50
            + df["norm_so_admired"] * 0.25
            + df["norm_so_desired"] * 0.25
        )
        print("[Processor] Scoring: Stack Overflow only (usage 50% + admired 25% + desired 25%)")

    else:
        # Fallback: equal weight
        df["Market_Dominance_Score"] = 0.0
        print("[Processor] WARNING: No data sources available for scoring")

    df["Market_Dominance_Score"] = df["Market_Dominance_Score"].round(4)
    return df


def inject_static_metadata(df: pd.DataFrame) -> pd.DataFrame:
    """Merge static Pros, Cons, and Audience_Label into the DataFrame."""
    df = df.copy()
    df["audience_label"] = df["framework"].map(
        lambda fw: STATIC_METADATA.get(fw, {}).get("audience_label", "")
    )
    df["pros"] = df["framework"].map(
        lambda fw: STATIC_METADATA.get(fw, {}).get("pros", [])
    )
    df["cons"] = df["framework"].map(
        lambda fw: STATIC_METADATA.get(fw, {}).get("cons", [])
    )
    return df


def export_outputs(df: pd.DataFrame, sources_used: list[str]) -> None:
    """Write processed CSV and JSON to disk."""
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # Add sources metadata column
    df = df.copy()
    df["sources_used"] = ", ".join(sources_used)

    # CSV – drop list columns (not CSV-friendly)
    csv_cols = [c for c in df.columns if c not in ("pros", "cons")]
    df[csv_cols].to_csv(CSV_OUTPUT, index=False, encoding="utf-8")
    print(f"[Processor] CSV  written to {CSV_OUTPUT}")

    # JSON – full DataFrame including lists
    json_df = df.copy()
    json_df["pros"] = json_df["pros"].apply(lambda x: x if isinstance(x, list) else [])
    json_df["cons"] = json_df["cons"].apply(lambda x: x if isinstance(x, list) else [])

    records = json_df.to_dict(orient="records")
    with open(JSON_OUTPUT, "w", encoding="utf-8") as fh:
        json.dump({
            "sources_used": sources_used,
            "frameworks": records,
        }, fh, indent=2, ensure_ascii=False)
    print(f"[Processor] JSON written to {JSON_OUTPUT}")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def process() -> pd.DataFrame:
    """Run the full processing pipeline and return the final DataFrame."""
    df, sources_used = load_raw_data()
    print(f"[Processor] Loaded {len(df)} frameworks, sources: {sources_used}")

    df = normalize_and_score(df, sources_used)
    df = inject_static_metadata(df)
    export_outputs(df, sources_used)
    return df


if __name__ == "__main__":
    process()
    print("[Processor] Done.")
