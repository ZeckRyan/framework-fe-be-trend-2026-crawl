"use client";

interface Framework {
  framework: string;
  category: string;
  stargazers_count: number;
  total_weekly_downloads: number;
  Market_Dominance_Score: number;
  stars?: number;
  audience_label: string;
  pros: string[];
  cons: string[];
  so_usage_pct?: number;
  so_admired_pct?: number;
  so_desired_pct?: number;
  sources_used?: string;
}

interface InfographicCardProps {
  data: Framework;
  maxScore?: number;
  maxStars?: number;
  maxDownloads?: number;
  accentColor?: string;
}

function formatNumber(num: number): string {
  if (num >= 1_000_000) return `${(num / 1_000_000).toFixed(1)}M`;
  if (num >= 1_000) return `${(num / 1_000).toFixed(1)}K`;
  return num.toString();
}

function pct(value: number, max: number): number {
  if (max <= 0) return 0;
  return Math.min(100, Math.round((value / max) * 100));
}

/** A thin horizontal bar visualizing a percentage */
function MetricBar({ label, value, displayValue, barColor }: { label: string; value: number; displayValue: string; barColor?: string }) {
  return (
    <div className="flex items-center gap-3">
      <span className="w-20 shrink-0 text-xs text-gray-500 dark:text-gray-400 truncate">{label}</span>
      <div className="flex-1 h-2 rounded-full bg-gray-100 dark:bg-gray-800 overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-500"
          style={{ width: `${Math.max(value, 1)}%`, backgroundColor: barColor || '#9CA3AF' }}
        />
      </div>
      <span className="w-14 shrink-0 text-right text-xs font-medium text-gray-700 dark:text-gray-300 tabular-nums">
        {displayValue}
      </span>
    </div>
  );
}

export default function InfographicCard({ data, maxScore = 1, maxStars = 1, maxDownloads = 1, accentColor }: InfographicCardProps) {
  const scorePct = pct(data.Market_Dominance_Score, maxScore);
  const starsPct = pct(data.stargazers_count, maxStars);
  const dlPct = pct(data.total_weekly_downloads, maxDownloads);

  const hasSO = (data.so_usage_pct ?? 0) > 0 || (data.so_admired_pct ?? 0) > 0;
  const hasCrawl = (data.stargazers_count ?? 0) > 0 || (data.total_weekly_downloads ?? 0) > 0;

  // Fallback bar color for when no accent is provided
  const barColor = accentColor || '#6B7280';

  return (
    <div className="flex flex-col rounded-xl border border-gray-200 dark:border-gray-700/60 bg-white dark:bg-gray-900/80 shadow-sm hover:shadow-md transition-shadow duration-200 group">
      <div className="flex flex-1 flex-col p-5">
        {/* Header */}
        <div className="flex items-baseline justify-between gap-2 mb-1">
          <h3 className="text-base font-semibold text-gray-900 dark:text-white">
            {data.framework}
          </h3>
          <span
            className="text-[11px] font-medium uppercase tracking-wider opacity-70"
            style={{ color: accentColor || undefined }}
          >
            {data.category}
          </span>
        </div>
        <p className="text-xs text-gray-500 dark:text-gray-400 mb-4">{data.audience_label}</p>

        {/* Star Rating */}
        <div className="mb-4">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[11px] uppercase tracking-wider text-gray-400 dark:text-gray-500">Rating</span>
            <span className="text-xl leading-none">
              <span style={{ color: accentColor || '#F59E0B' }}>{"★".repeat(data.stars ?? 3)}</span>
              <span className="text-gray-200 dark:text-gray-700">{"★".repeat(5 - (data.stars ?? 3))}</span>
            </span>
          </div>
          <div className="h-1.5 rounded-full bg-gray-100 dark:bg-gray-800 overflow-hidden">
            <div
              className="h-full rounded-full transition-all duration-700"
              style={{ width: `${Math.max(scorePct, 2)}%`, backgroundColor: barColor }}
            />
          </div>
        </div>

        {/* Crawl metrics as bars */}
        {hasCrawl && (
          <div className="space-y-2 mb-4">
            <MetricBar label="Stars" value={starsPct} displayValue={formatNumber(data.stargazers_count)} barColor={barColor} />
            <MetricBar label="Downloads" value={dlPct} displayValue={formatNumber(data.total_weekly_downloads)} barColor={barColor} />
          </div>
        )}

        {/* SO metrics as compact rows */}
        {hasSO && (
          <div className="space-y-2 mb-4 pt-3 border-t border-gray-100 dark:border-gray-800">
            <p className="text-[10px] uppercase tracking-wider text-gray-400 dark:text-gray-500 mb-1">
              SO Survey 2025
            </p>
            <MetricBar label="Usage" value={pct(data.so_usage_pct ?? 0, 50)} displayValue={`${(data.so_usage_pct ?? 0).toFixed(1)}%`} barColor={barColor} />
            <MetricBar label="Admired" value={pct(data.so_admired_pct ?? 0, 80)} displayValue={`${(data.so_admired_pct ?? 0).toFixed(1)}%`} barColor={barColor} />
            <MetricBar label="Desired" value={pct(data.so_desired_pct ?? 0, 35)} displayValue={`${(data.so_desired_pct ?? 0).toFixed(1)}%`} barColor={barColor} />
          </div>
        )}

        {/* Pros & Cons */}
        <div className="mt-auto pt-3 border-t border-gray-100 dark:border-gray-800 space-y-2">
          {data.pros.length > 0 && (
            <ul className="space-y-0.5">
              {data.pros.map((pro, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
                  <span className="mt-px select-none" style={{ color: accentColor || '#9CA3AF' }}>+</span>
                  <span>{pro}</span>
                </li>
              ))}
            </ul>
          )}
          {data.cons.length > 0 && (
            <ul className="space-y-0.5">
              {data.cons.map((con, i) => (
                <li key={i} className="flex items-start gap-2 text-xs text-gray-500 dark:text-gray-500 leading-relaxed">
                  <span className="mt-px text-gray-300 dark:text-gray-600 select-none">−</span>
                  <span>{con}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
