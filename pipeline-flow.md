# Framework Trends Tracker — Pipeline Flow

```mermaid
graph TD
    subgraph 1. Data Crawling
        A[api_clients.py<br/>FRAMEWORK_REGISTRY<br/>18 frameworks] -->|"GitHubClient.get_metrics()"| B[GitHub API<br/>stars, forks, issues]
        A -->|"NPMClient.get_weekly_downloads()"| C[NPM API<br/>weekly downloads]
        A -->|"PyPIClient.get_weekly_downloads()"| D[PyPI API<br/>weekly downloads]
        A -->|"StackOverflowClient.get_metrics()"| E[SO 2025 Survey<br/>usage, admired, desired]
        B --> F[main_pipeline.py<br/>run_pipeline --sources]
        C --> F
        D --> F
        E --> F
    end

    subgraph 2. Data Processing
        F -->|"json.dump()"| G[raw_framework_data.json]
        G -->|"load_raw_data()"| H[data_processor.py]
        H -->|"_min_max_normalize()"| I[Min-Max Normalization<br/>0.0 - 1.0]
        I -->|"normalize_and_score()"| J[Market_Dominance_Score<br/>stars 20% + downloads 30%<br/>+ usage 25% + admired 12.5%<br/>+ desired 12.5%]
        J -->|"inject_static_metadata()"| K[pros, cons, audience_label]
        K -->|"export_outputs()"| L[processed_framework_data<br/>.csv + .json]
    end

    subgraph 3. Internal Report
        L -->|"pd.read_csv()"| M[generate_report.py]
        M -->|"generate_downloads_vs_stars_chart()"| N[downloads_vs_stars.png]
        M -->|"generate_market_dominance_chart()"| O[market_dominance_score.png]
        M -->|"generate_stackoverflow_chart()"| P[stackoverflow_survey.png]
        M -->|"generate_markdown_report()"| Q[internal_report.md]
    end

    subgraph 4. Client Dashboard
        L -->|"import JSON"| R[page.tsx<br/>Hero + Sections + Recommendations]
        R --> S[InfographicCard.tsx<br/>Score bars + SO metrics + pros/cons]
        R --> T[FrameworkChart.tsx<br/>Ranking bars by category]
        R --> U[RecGroup<br/>Project Kecil / Sedang / Besar]
        S --> V[Dashboard<br/>localhost:3000]
        T --> V
        U --> V
    end
```

## File Summary

| # | File | Function | Output |
|---|------|----------|--------|
| 1 | `scraper/api_clients.py` | Crawl GitHub, NPM, PyPI APIs | Raw metrics per framework |
| 2 | `scraper/stackoverflow_client.py` | SO 2025 survey data | Usage %, Admired %, Desired % |
| 3 | `scraper/main_pipeline.py` | Orchestrate all crawlers | `raw_framework_data.json` |
| 4 | `scraper/data_processor.py` | Normalize + score + metadata | `processed_framework_data.json` |
| 5 | `reports_internal/generate_report.py` | Plotly charts + markdown | 3 PNGs + `internal_report.md` |
| 6 | `client_dashboard/src/app/page.tsx` | Hero orbit + sections + recs | Interactive web page |
| 7 | `src/components/InfographicCard.tsx` | Framework card with bars | 18 cards (8 FE + 10 BE) |
| 8 | `src/components/FrameworkChart.tsx` | CSS ranking chart | Frontend vs Backend ranking |

## Scoring Formula (All Sources Combined)

```
Market_Dominance_Score =
  (norm_stars        × 0.20)  ← GitHub community interest
+ (norm_downloads    × 0.30)  ← NPM/PyPI production adoption
+ (norm_so_usage     × 0.25)  ← SO 2025 industry usage
+ (norm_so_admired   × 0.125) ← SO 2025 satisfaction
+ (norm_so_desired   × 0.125) ← SO 2025 growth potential
```

## 3 Scoring Modes

| Mode | Sources | Formula |
|------|---------|---------|
| **Combined** | All | Stars 20% + Downloads 30% + Usage 25% + Admired 12.5% + Desired 12.5% |
| **Crawl-only** | GitHub + NPM/PyPI | Stars 40% + Downloads 60% |
| **SO-only** | Stack Overflow | Usage 50% + Admired 25% + Desired 25% |
