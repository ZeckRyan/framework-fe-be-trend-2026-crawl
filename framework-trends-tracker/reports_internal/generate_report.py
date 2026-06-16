"""
Internal report generator.
Reads processed_framework_data.csv, generates Plotly charts,
and writes an analytical Markdown report.
Adapts charts/content based on which data sources were used.
"""

import os
from datetime import datetime, timezone

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_INPUT = os.path.join(PROJECT_ROOT, "data", "processed", "processed_framework_data.csv")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "reports_internal", "output")
CHARTS_DIR = os.path.join(OUTPUT_DIR, "charts")
REPORT_FILE = os.path.join(OUTPUT_DIR, "internal_report.md")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _get_sources(df: pd.DataFrame) -> list[str]:
    """Read sources_used from the CSV (all rows have the same value)."""
    raw = df["sources_used"].dropna().iloc[0] if "sources_used" in df.columns else ""
    return [s.strip() for s in str(raw).split(",") if s.strip()]


def _has_so_data(df: pd.DataFrame) -> bool:
    return "so_usage_pct" in df.columns and df["so_usage_pct"].sum() > 0


def _has_crawl_data(df: pd.DataFrame) -> bool:
    return "stargazers_count" in df.columns and df["stargazers_count"].sum() > 0


# ---------------------------------------------------------------------------
# Chart generation
# ---------------------------------------------------------------------------

def generate_downloads_vs_stars_chart(df: pd.DataFrame) -> str | None:
    """Bar chart comparing Downloads vs Stars across frameworks. Returns saved file path."""
    if not _has_crawl_data(df):
        print("[Report] Skipping downloads_vs_stars chart (no crawl data)")
        return None

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Stars (GitHub)",
        x=df["framework"],
        y=df["stargazers_count"],
        marker_color="#636EFA",
    ))

    fig.add_trace(go.Bar(
        name="Weekly Downloads",
        x=df["framework"],
        y=df["total_weekly_downloads"],
        marker_color="#EF553B",
    ))

    fig.update_layout(
        title="Unduhan Mingguan vs Bintang GitHub per Framework",
        barmode="group",
        xaxis_title="Framework",
        yaxis_title="Jumlah",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=20, t=80, b=60),
    )

    path = os.path.join(CHARTS_DIR, "downloads_vs_stars.png")
    fig.write_image(path, width=1200, height=600, scale=2)
    print(f"[Report] Chart saved: {path}")
    return path


def generate_stackoverflow_chart(df: pd.DataFrame) -> str | None:
    """Stacked bar chart showing SO usage/admired/desired. Returns saved file path."""
    if not _has_so_data(df):
        print("[Report] Skipping stackoverflow chart (no SO data)")
        return None

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Usage % (All Respondents)",
        x=df["framework"],
        y=df["so_usage_pct"],
        marker_color="#F47F20",
    ))
    fig.add_trace(go.Bar(
        name="Admired % (want to continue)",
        x=df["framework"],
        y=df["so_admired_pct"],
        marker_color="#636EFA",
    ))
    fig.add_trace(go.Bar(
        name="Desired % (want to learn)",
        x=df["framework"],
        y=df["so_desired_pct"],
        marker_color="#00CC96",
    ))

    fig.update_layout(
        title="Stack Overflow Developer Survey 2025 – Usage / Admired / Desired",
        barmode="group",
        xaxis_title="Framework",
        yaxis_title="Persentase (%)",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=20, t=80, b=60),
    )

    path = os.path.join(CHARTS_DIR, "stackoverflow_survey.png")
    fig.write_image(path, width=1200, height=600, scale=2)
    print(f"[Report] Chart saved: {path}")
    return path


def generate_market_dominance_chart(df: pd.DataFrame) -> str:
    """Horizontal bar chart ranking frameworks by Market_Dominance_Score. Returns saved file path."""
    sorted_df = df.sort_values("Market_Dominance_Score", ascending=True)

    fig = px.bar(
        sorted_df,
        x="Market_Dominance_Score",
        y="framework",
        orientation="h",
        title="Peringkat Market Dominance Score",
        color="category",
        color_discrete_map={"Frontend": "#636EFA", "Backend": "#00CC96"},
        labels={"Market_Dominance_Score": "Skor", "framework": "Framework", "category": "Kategori"},
        template="plotly_white",
    )

    fig.update_layout(
        margin=dict(l=120, r=20, t=80, b=40),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    path = os.path.join(CHARTS_DIR, "market_dominance_score.png")
    fig.write_image(path, width=1000, height=700, scale=2)
    print(f"[Report] Chart saved: {path}")
    return path


# ---------------------------------------------------------------------------
# Markdown report builder
# ---------------------------------------------------------------------------

def generate_markdown_report(df: pd.DataFrame, sources: list[str]) -> str:
    """Build the full internal_report.md content."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    has_crawl = _has_crawl_data(df)
    has_so = _has_so_data(df)

    ranked = df.sort_values("Market_Dominance_Score", ascending=False).reset_index(drop=True)

    md = []

    # --- Header ---
    md.append("# Laporan Internal: Tren Framework 2026")
    md.append("")
    md.append(f"**Tanggal Eksekusi:** {now}")
    md.append(f"**Sumber Data:** {', '.join(s.title() for s in sources)}")
    md.append("")
    md.append("---")
    md.append("")

    # --- Executive Summary ---
    md.append("## Ringkasan Eksekutif")
    md.append("")
    top_fw = ranked.iloc[0]

    source_desc = []
    if has_crawl:
        source_desc.append("metrik GitHub (bintang, fork, issues) dan volume unduhan mingguan (NPM + PyPI)")
    if has_so:
        source_desc.append("data Stack Overflow Developer Survey 2025 (usage, admired, desired)")
    source_text = " serta ".join(source_desc) if source_desc else "data yang tersedia"

    md.append(
        f"Berdasarkan analisis {source_text}, "
        f"**{top_fw['framework']}** menempati peringkat teratas dengan "
        f"**Market Dominance Score {top_fw['Market_Dominance_Score']:.4f}**. "
        f"Framework ini menunjukkan dominasi kuat baik dari sisi popularitas komunitas maupun adopsi aktual di industri."
    )
    md.append("")

    frontend_top = ranked[ranked["category"] == "Frontend"].iloc[0]
    backend_top = ranked[ranked["category"] == "Backend"].iloc[0]
    md.append(f"- **Frontend Leader:** {frontend_top['framework']} (skor {frontend_top['Market_Dominance_Score']:.4f})")
    md.append(f"- **Backend Leader:** {backend_top['framework']} (skor {backend_top['Market_Dominance_Score']:.4f})")
    md.append("")

    # --- Chart: Downloads vs Stars ---
    if has_crawl:
        md.append("## Perbandingan Unduhan vs Bintang")
        md.append("")
        md.append("![Unduhan vs Bintang](charts/downloads_vs_stars.png)")
        md.append("")
        md.append(
            "Grafik batang di atas membandingkan jumlah bintang GitHub (biru) dengan volume unduhan "
            "mingguan (merah) untuk setiap framework. Perbedaan signifikan antara kedua metrik dapat "
            "mengindikasikan framework yang populer secara komunitas namun belum tentu paling banyak "
            "digunakan di production, atau sebaliknya."
        )
        md.append("")

    # --- Chart: Stack Overflow ---
    if has_so:
        md.append("## Stack Overflow Developer Survey 2025")
        md.append("")
        md.append("![Stack Overflow Survey](charts/stackoverflow_survey.png)")
        md.append("")
        md.append(
            "Grafik ini menampilkan tiga metrik dari Stack Overflow Developer Survey 2025:"
        )
        md.append("")
        md.append("- **Usage %** – persentase responden yang menggunakan framework dalam setahun terakhir")
        md.append("- **Admired %** – persentase pengguna yang ingin terus menggunakannya")
        md.append("- **Desired %** – persentase non-pengguna yang ingin mempelajarinya")
        md.append("")
        md.append(
            "*Sumber: [Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/technology), "
            "23,678 responden, lisensi Open Database License (ODbL).*"
        )
        md.append("")

        # SO insights table
        md.append("| Framework | Usage % | Admired % | Desired % |")
        md.append("|-----------|--------:|----------:|----------:|")
        for _, row in ranked.iterrows():
            md.append(
                f"| {row['framework']} | {row.get('so_usage_pct', 0):.1f}% "
                f"| {row.get('so_admired_pct', 0):.1f}% "
                f"| {row.get('so_desired_pct', 0):.1f}% |"
            )
        md.append("")

    # --- Chart: Market Dominance Score ---
    md.append("## Peringkat Market Dominance Score")
    md.append("")
    md.append("![Market Dominance Score](charts/market_dominance_score.png)")
    md.append("")

    if has_crawl and has_so:
        md.append(
            "Skor komposit ini dihitung dengan formula gabungan: "
            "`Score = (norm_stars * 0.2) + (norm_downloads * 0.3) + "
            "(norm_so_usage * 0.25) + (norm_so_admired * 0.125) + (norm_so_desired * 0.125)`. "
            "Bobot terbagi seimbang antara data crawl (50%) dan survei Stack Overflow (50%)."
        )
    elif has_crawl:
        md.append(
            "Skor komposit ini dihitung dengan formula: `Score = (norm_stars * 0.4) + (norm_downloads * 0.6)`. "
            "Bobot unduhan lebih tinggi (60%) karena mencerminkan adopsi aktual di production environment, "
            "sedangkan bintang lebih mencerminkan popularitas/hype komunitas."
        )
    elif has_so:
        md.append(
            "Skor komposit ini dihitung dengan formula: `Score = (norm_so_usage * 0.5) + "
            "(norm_so_admired * 0.25) + (norm_so_desired * 0.25)`. "
            "Usage mendapatkan bobot tertinggi karena mencerminkan adopsi aktual di industri."
        )
    md.append("")

    # --- Ranking Table ---
    md.append("## Tabel Peringkat Lengkap")
    md.append("")

    if has_crawl and has_so:
        md.append("| # | Framework | Kategori | Stars | Downloads | SO Usage% | Skor |")
        md.append("|---|-----------|----------|------:|----------:|----------:|-----:|")
        for i, row in ranked.iterrows():
            idx = ranked.index.get_loc(i) + 1
            md.append(
                f"| {idx} | {row['framework']} | {row['category']} "
                f"| {row['stargazers_count']:,} | {row['total_weekly_downloads']:,} "
                f"| {row.get('so_usage_pct', 0):.1f}% "
                f"| {row['Market_Dominance_Score']:.4f} |"
            )
    elif has_crawl:
        md.append("| # | Framework | Kategori | Stars | Downloads | Skor |")
        md.append("|---|-----------|----------|------:|----------:|-----:|")
        for i, row in ranked.iterrows():
            idx = ranked.index.get_loc(i) + 1
            md.append(
                f"| {idx} | {row['framework']} | {row['category']} "
                f"| {row['stargazers_count']:,} | {row['total_weekly_downloads']:,} "
                f"| {row['Market_Dominance_Score']:.4f} |"
            )
    elif has_so:
        md.append("| # | Framework | Kategori | SO Usage% | SO Admired% | SO Desired% | Skor |")
        md.append("|---|-----------|----------|----------:|------------:|------------:|-----:|")
        for i, row in ranked.iterrows():
            idx = ranked.index.get_loc(i) + 1
            md.append(
                f"| {idx} | {row['framework']} | {row['category']} "
                f"| {row.get('so_usage_pct', 0):.1f}% "
                f"| {row.get('so_admired_pct', 0):.1f}% "
                f"| {row.get('so_desired_pct', 0):.1f}% "
                f"| {row['Market_Dominance_Score']:.4f} |"
            )
    md.append("")

    # --- Architecture Flow Comparison ---
    md.append("## Analisis Arsitektur: Perbandingan Paradigma Framework")
    md.append("")

    # Dynamically pick top 2 frontend for comparison
    fe_top2 = ranked[ranked["category"] == "Frontend"].head(2)
    if len(fe_top2) >= 2:
        f1, f2 = fe_top2.iloc[0]["framework"], fe_top2.iloc[1]["framework"]
        md.append(f"### Head-to-Head: {f1} vs {f2} (Top 2 Frontend)")
        md.append("")

    md.append("| Aspek | React (JSX) | Vue.js (SFC) | Svelte (Compiler) | Angular (Opinionated) |")
    md.append("|-------|-----------|----------------|------------------|--------------------|")
    md.append("| Paradigma | JSX (JavaScript-first) | Template + Script + Style | Compile-time reactivity | TypeScript DI + Decorator |")
    md.append("| State Mgmt | Hooks / Redux / Zustand | Composition API / Pinia | Stores / runes | Signals / NgRx |")
    md.append("| Learning Curve | Menengah–Tinggi | Rendah–Menengah | Rendah | Tinggi |")
    md.append("| Bundle Size | ~45KB + ReactDOM | ~40KB gzip | Paling ringan (compiler) | Besar (>100KB) |")
    md.append("| Enterprise Meta | Next.js | Nuxt | — | Built-in |")
    md.append("")

    md.append("### Backend Paradigm Comparison")
    md.append("")
    md.append("| Framework | Language | Paradigma | Async | Real-time |")
    md.append("|-----------|----------|-----------|-------|-----------|")
    md.append("| FastAPI | Python | Micro, async-first | ✅ Native | Via WebSockets |")
    md.append("| Express.js | JavaScript | Micro, minimalis | Via middleware | Socket.io |")
    md.append("| Spring Boot | Java | Opinionated, DI | Spring WebFlux | Spring WebSocket |")
    md.append("| Django | Python | Full-stack, batteries-included | Django Channels | Channels / Daphne |")
    md.append("| Flask | Python | Micro, fleksibel | Via extensions | Flask-SocketIO |")
    md.append("| NestJS | TypeScript | Modular, DI-heavy | ✅ Native | @nestjs/websockets |")
    md.append("| Laravel | PHP | Full-stack, elegant | Via Octane | Laravel Reverb |")
    md.append("| Ruby on Rails | Ruby | Convention over config | Via ActionCable | ActionCable |")
    md.append("| Phoenix | Elixir | Functional, BEAM VM | ✅ Native | Phoenix Channels |")
    md.append("| ASP.NET Core | C# | Enterprise, cross-platform | ✅ Kestrel | SignalR |")
    md.append("")

    # --- Technical Recommendations ---
    md.append("## Rekomendasi Teknis")
    md.append("")
    md.append(
        "Berdasarkan hasil analisis metrik dan karakteristik arsitektur masing-masing framework, "
        "berikut rekomendasi penggunaan berdasarkan spesifikasi tim:"
    )
    md.append("")
    md.append("| Spesifikasi Tim | Rekomendasi Frontend | Rekomendasi Backend | Alasan |")
    md.append("|-----------------|---------------------|--------------------:|--------|")
    md.append("| Tim kecil (2-5), MVP cepat | Vue.js / Svelte | FastAPI / Flask | Learning curve rendah, time-to-market tercepat |")
    md.append("| Tim menengah (5-15), SaaS | Next.js / Remix | Express.js / NestJS | SSR bawaan, ekosistem middleware luas |")
    md.append("| Enterprise besar (15+), long-term | Angular | Spring Boot / ASP.NET Core | Arsitektur opinionated, dukungan enterprise |")
    md.append("| Tim data/AI, integrasi ML | React | FastAPI | Ekosistem React untuk viz, async FastAPI untuk inference |")
    md.append("| Content/marketing site | Astro | Laravel / Django | Zero-JS performance, CMS-ready backend |")
    md.append("| Real-time / chat app | React / Vue.js | Phoenix / NestJS | Phoenix Channels / WebSocket native |")
    md.append("| Legacy migration | React / Nuxt | Django / Ruby on Rails | Batteries-included, rapid migration |")
    md.append("| Startup bootstrapping | Svelte / Astro | Laravel / Rails | Convention over config, fastest delivery |")
    md.append("")

    md.append("---")
    md.append("")
    md.append(f"*Laporan ini di-generate secara otomatis oleh Framework Trends Tracker pada {now}.*")
    md.append("")

    return "\n".join(md)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def generate() -> None:
    """Run chart generation and Markdown report writing."""
    os.makedirs(CHARTS_DIR, exist_ok=True)

    df = pd.read_csv(CSV_INPUT)
    sources = _get_sources(df)
    print(f"[Report] Loaded {len(df)} frameworks from {CSV_INPUT}")
    print(f"[Report] Sources: {sources}")

    generate_downloads_vs_stars_chart(df)
    generate_stackoverflow_chart(df)
    generate_market_dominance_chart(df)

    md_content = generate_markdown_report(df, sources)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(REPORT_FILE, "w", encoding="utf-8") as fh:
        fh.write(md_content)

    print(f"[Report] Markdown report written to {REPORT_FILE}")


if __name__ == "__main__":
    generate()
    print("[Report] Done.")
