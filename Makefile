.PHONY: install run crawl process report dashboard dev build clean help

# ── Default: run full pipeline ──
run: crawl process report
	@echo "Done: full pipeline complete."

# ─ Help ──
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "Pipeline:"
	@echo "  run        Run full pipeline (crawl + process + report)"
	@echo "  crawl      Crawl data from GitHub, NPM, PyPI, SO"
	@echo "  process    Normalize & score raw data"
	@echo "  report     Generate internal report + charts"
	@echo ""
	@echo "Dashboard:"
	@echo "  dev        Start Next.js dev server (localhost:3000)"
	@echo "  build      Build Next.js for production"
	@echo ""
	@echo "Setup:"
	@echo "  install    Install Python + Node.js dependencies"
	@echo "  clean      Remove build artifacts"

# ── Python Pipeline ──
crawl:
	@echo "=== Phase 1: Crawling ==="
	cd framework-trends-tracker && python -m scraper.main_pipeline

process:
	@echo "=== Phase 2: Processing & Scoring ==="
	cd framework-trends-tracker && python -m scraper.data_processor

report:
	@echo "=== Phase 3: Internal Report ==="
	cd framework-trends-tracker && python -m reports_internal.generate_report

# ── Selective Sources ──
crawl-all:
	cd framework-trends-tracker && python -m scraper.main_pipeline --sources github npm pypi stackoverflow

crawl-github:
	cd framework-trends-tracker && python -m scraper.main_pipeline --sources github

crawl-so:
	cd framework-trends-tracker && python -m scraper.main_pipeline --sources stackoverflow

# ── Dashboard ──
dev:
	npm run dev --prefix client_dashboard

build:
	npm run build --prefix client_dashboard

# ── Setup ──
install:
	cd framework-trends-tracker && pip install -r requirements.txt
	cd client_dashboard && npm install

# ── Cleanup ──
clean:
	rm -rf framework-trends-tracker/data/processed/*
	rm -rf framework-trends-tracker/reports_internal/output/charts/*
	rm -rf framework-trends-tracker/reports_internal/output/internal_report.md
	rm -rf client_dashboard/.next
	rm -rf client_dashboard/out
