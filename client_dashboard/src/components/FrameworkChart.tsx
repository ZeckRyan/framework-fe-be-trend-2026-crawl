"use client";

interface Framework {
  framework: string;
  category: string;
  Market_Dominance_Score: number;
  so_usage_pct?: number;
}

interface FrameworkChartProps {
  data: Framework[];
}

export default function FrameworkChart({ data }: FrameworkChartProps) {
  const sorted = [...data].sort((a, b) => b.Market_Dominance_Score - a.Market_Dominance_Score);
  const maxScore = sorted[0]?.Market_Dominance_Score ?? 1;

  const frontend = sorted.filter((f) => f.category === "Frontend");
  const backend = sorted.filter((f) => f.category === "Backend");

  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-700/60 bg-white dark:bg-gray-900/80 p-6 shadow-sm">
      <h3 className="text-base font-semibold text-gray-900 dark:text-white mb-1">
        Market Dominance Ranking
      </h3>
      <p className="text-xs text-gray-500 dark:text-gray-400 mb-6">
        18 frameworks scored across GitHub, NPM/PyPI downloads & SO 2025 survey
      </p>

      <div className="space-y-6">
        <RankingGroup title="Frontend" items={frontend} maxScore={maxScore} color="#3B82F6" />
        <RankingGroup title="Backend" items={backend} maxScore={maxScore} color="#14B8A6" />
      </div>
    </div>
  );
}

function RankingGroup({ title, items, maxScore, color }: { title: string; items: Framework[]; maxScore: number; color: string }) {
  return (
    <div>
      <p className="text-[11px] uppercase tracking-wider font-medium mb-2.5" style={{ color }}>
        {title}
      </p>
      <div className="space-y-1.5">
        {items.map((fw) => {
          const barWidth = maxScore > 0 ? (fw.Market_Dominance_Score / maxScore) * 100 : 0;
          return (
            <div key={fw.framework} className="flex items-center gap-3 group">
              <span className="w-24 shrink-0 text-xs text-gray-600 dark:text-gray-400 truncate group-hover:text-gray-900 dark:group-hover:text-white transition-colors">
                {fw.framework}
              </span>
              <div className="flex-1 h-4 rounded bg-gray-50 dark:bg-gray-800/50 overflow-hidden">
                <div
                  className="h-full rounded transition-all duration-700"
                  style={{ width: `${Math.max(barWidth, 1)}%`, backgroundColor: color, opacity: 0.65 }}
                />
              </div>
              <span className="w-12 shrink-0 text-right text-xs font-medium text-gray-500 dark:text-gray-400 tabular-nums">
                {fw.Market_Dominance_Score.toFixed(2)}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
