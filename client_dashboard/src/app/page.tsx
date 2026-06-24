import InfographicCard from "@/components/InfographicCard";
import FrameworkChart from "@/components/FrameworkChart";
import data from "@/data/processed_framework_data.json";

interface Framework {
  framework: string;
  category: string;
  github_repo: string;
  stargazers_count: number;
  forks_count: number;
  open_issues_count: number;
  npm_weekly_downloads: number;
  pypi_weekly_downloads: number;
  total_weekly_downloads: number;
  norm_stargazers_count: number;
  norm_total_weekly_downloads: number;
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

const frameworks: Framework[] = data.frameworks as Framework[];

/* ── Orbit icon helpers ── */
const orbitIcons = [
  { src: "/icons/react.png", label: "React" },
  { src: "/icons/vue.png", label: "Vue" },
  { src: "/icons/angular.png", label: "Angular" },
  { src: "/icons/django.png", label: "Django" },
  { src: "/icons/laravel.png", label: "Laravel" },
  { src: "/icons/golang.png", label: "Go" },
  { src: "/icons/react.png", label: "Next.js" },
  { src: "/icons/vue.png", label: "Nuxt" },
  { src: "/icons/angular.png", label: "Svelte" },
  { src: "/icons/django.png", label: "Flask" },
  { src: "/icons/laravel.png", label: "NestJS" },
  { src: "/icons/golang.png", label: "Phoenix" },
];

const outerIcons = [
  { src: "/icons/vue.png", label: "Remix" },
  { src: "/icons/react.png", label: "Astro" },
  { src: "/icons/angular.png", label: "Ruby" },
  { src: "/icons/django.png", label: "Express" },
  { src: "/icons/laravel.png", label: "ASP.NET" },
  { src: "/icons/golang.png", label: "Spring" },
  { src: "/icons/react.png", label: "FastAPI" },
  { src: "/icons/vue.png", label: "Nuxt" },
];

/* ── Recommendation group component ── */
function RecGroup({ title, subtitle, color, items }: {
  title: string;
  subtitle: string;
  color: string;
  items: { title: string; stack: string; body: string }[];
}) {
  return (
    <div>
      <div className="flex items-center gap-3 mb-3">
        <div className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: color }} />
        <div>
          <h3 className="text-sm font-semibold text-gray-900 dark:text-white">{title}</h3>
          <p className="text-[11px] text-gray-400 dark:text-gray-500">{subtitle}</p>
        </div>
      </div>
      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3 ml-5">
        {items.map((item) => (
          <div key={item.title} className="rounded-lg bg-white dark:bg-gray-900 border border-gray-150 dark:border-gray-800 p-4">
            <h4 className="text-xs font-semibold text-gray-900 dark:text-white mb-1">{item.title}</h4>
            <p className="text-[11px] font-medium mb-2" style={{ color }}>
              {item.stack}
            </p>
            <p className="text-[11px] text-gray-500 dark:text-gray-400 leading-relaxed">{item.body}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function Home() {
  const frontendFrameworks = frameworks.filter((fw) => fw.category === "Frontend");
  const backendFrameworks = frameworks.filter((fw) => fw.category === "Backend");
  const sortedByScore = [...frameworks].sort(
    (a, b) => b.Market_Dominance_Score - a.Market_Dominance_Score
  );
  const topFramework = sortedByScore[0];

  const maxScore = Math.max(...frameworks.map((f) => f.Market_Dominance_Score), 0.01);
  const maxStars = Math.max(...frameworks.map((f) => f.stargazers_count), 1);
  const maxDownloads = Math.max(...frameworks.map((f) => f.total_weekly_downloads), 1);

  return (
    <main className="min-h-screen bg-white dark:bg-gray-950">
      {/* ════════════════════ HERO ════════════════════ */}
      <section className="relative h-screen overflow-hidden">
        {/* Subtle radial tint background */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(59,130,246,0.05),transparent_65%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_70%_60%,rgba(20,184,166,0.04),transparent_55%)]" />

        {/* Faint dot texture */}
        <div
          className="absolute inset-0 opacity-[0.015] dark:opacity-[0.03]"
          style={{
            backgroundImage: 'radial-gradient(circle, currentColor 1px, transparent 1px)',
            backgroundSize: '20px 20px',
          }}
        />

        <div className="relative h-full mx-auto max-w-7xl px-6 lg:px-8">
          {/* ── Orbit wrapper: ring encircles ALL hero content ── */}
          <div className="relative flex items-center justify-center h-full">

            {/* ── Inner orbit ring (12 icons, clockwise) ── */}
            <div className="orbit-ring absolute left-1/2 top-1/2 pointer-events-none" style={{ width: '520px', height: '520px', marginLeft: '-260px', marginTop: '-260px' }}>
              {orbitIcons.map((icon, i) => {
                const angle = (i * 360) / orbitIcons.length;
                return (
                  <div
                    key={`inner-${i}`}
                    className="absolute left-1/2 top-1/2"
                    style={{ transform: `rotate(${angle}deg) translateY(-260px)` }}
                  >
                    <img
                      src={icon.src}
                      alt=""
                      aria-hidden="true"
                      className="orbit-icon w-7 h-7 opacity-40 dark:opacity-30 select-none pointer-events-none"
                      style={{ animationDelay: `${-(i * (40 / orbitIcons.length))}s` }}
                    />
                  </div>
                );
              })}
            </div>

            {/* ── Outer orbit ring (8 icons, counter-clockwise) ── */}
            <div className="orbit-ring-reverse absolute left-1/2 top-1/2 pointer-events-none" style={{ width: '650px', height: '650px', marginLeft: '-325px', marginTop: '-325px' }}>
              {outerIcons.map((icon, i) => {
                const angle = (i * 360) / outerIcons.length;
                return (
                  <div
                    key={`outer-${i}`}
                    className="absolute left-1/2 top-1/2"
                    style={{ transform: `rotate(${angle}deg) translateY(-325px)` }}
                  >
                    <img
                      src={icon.src}
                      alt=""
                      aria-hidden="true"
                      className="orbit-icon-reverse w-5 h-5 opacity-25 dark:opacity-20 select-none pointer-events-none"
                      style={{ animationDelay: `${-(i * (55 / outerIcons.length))}s` }}
                    />
                  </div>
                );
              })}
            </div>

            {/* ── Faint orbit path circles ── */}
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[520px] h-[520px] rounded-full border border-dashed border-gray-300/40 dark:border-gray-600/25 pointer-events-none" />
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[650px] h-[650px] rounded-full border border-dashed border-gray-300/25 dark:border-gray-600/15 pointer-events-none" />

            {/* ── ALL hero content centered inside the orbit ── */}
            <div className="relative z-10 flex flex-col items-center text-center px-6">
              {/* Heading with color */}
              <p className="text-xs font-medium uppercase tracking-[0.2em] mb-4" style={{ color: '#3B82F6' }}>
                Laporan Infografis 2026
              </p>
              <h1 className="text-3xl font-bold tracking-tight sm:text-4xl lg:text-5xl">
                <span className="text-gray-900 dark:text-white">Tren Framework</span>
                <span className="block mt-1" style={{ color: '#14B8A6' }}>
                  yang Menguasai Industri
                </span>
              </h1>
              <p className="mt-4 text-sm leading-6 text-gray-500 dark:text-gray-400 max-w-md">
                Analisis komparatif 18 framework frontend &amp; backend berdasarkan
                metrik GitHub, volume unduhan, dan Stack Overflow Developer Survey 2025.
              </p>

              {/* CTA Buttons */}
              <div className="flex flex-col sm:flex-row items-center gap-4 mt-8">
                <a
                  href="#frontend"
                  className="inline-flex items-center gap-2.5 rounded-full px-6 py-3 text-sm font-semibold text-white shadow-md shadow-blue-500/20 transition-all hover:shadow-lg hover:shadow-blue-500/30 hover:scale-[1.03] active:scale-[0.98]"
                  style={{ backgroundColor: '#3B82F6' }}
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 17.25v1.007a3 3 0 0 1-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0 1 15 18.257V17.25m6-12V15a2.25 2.25 0 0 1-2.25 2.25H5.25A2.25 2.25 0 0 1 3 15V5.25m18 0A2.25 2.25 0 0 0 18.75 3H5.25A2.25 2.25 0 0 0 3 5.25m18 0H3" />
                  </svg>
                  Frontend Framework
                </a>
                <a
                  href="#backend"
                  className="inline-flex items-center gap-2.5 rounded-full px-6 py-3 text-sm font-semibold text-white shadow-md shadow-teal-500/20 transition-all hover:shadow-lg hover:shadow-teal-500/30 hover:scale-[1.03] active:scale-[0.98]"
                  style={{ backgroundColor: '#14B8A6' }}
                >
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 14.25h13.5m-13.5 0a3 3 0 0 1-3-3m3 3a3 3 0 1 0 0 6h13.5a3 3 0 1 0 0-6m-16.5-3a3 3 0 0 1 3-3h13.5a3 3 0 0 1 3 3m-19.5 0a4.5 4.5 0 0 1 .9-2.7L5.737 5.1a3.375 3.375 0 0 1 2.7-1.35h7.126c1.062 0 2.062.5 2.7 1.35l2.587 3.45a4.5 4.5 0 0 1 .9 2.7m0 0a3 3 0 0 1-3 3m0 3h.008v.008h-.008v-.008Zm0-6h.008v.008h-.008v-.008Zm-3 6h.008v.008h-.008v-.008Zm0-6h.008v.008h-.008v-.008Z" />
                  </svg>
                  Backend Framework
                </a>
              </div>

              {/* Stats row */}
              <div className="flex items-center justify-center gap-8 mt-8 text-xs text-gray-400 dark:text-gray-500">
                <span><strong className="text-gray-600 dark:text-gray-300">18</strong> framework</span>
                <span className="w-1 h-1 rounded-full bg-gray-300 dark:bg-gray-600" />
                <span><strong className="text-gray-600 dark:text-gray-300">4</strong> sumber data</span>
                <span className="w-1 h-1 rounded-full bg-gray-300 dark:bg-gray-600" />
                <span>Top: <strong className="text-gray-600 dark:text-gray-300">{topFramework.framework}</strong></span>
              </div>
            </div>
          </div>
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 flex flex-col items-center gap-1 text-gray-300 dark:text-gray-600 animate-bounce">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
          </svg>
        </div>
      </section>

      {/* ════════════════ RANKING CHART ════════════════ */}
      <section className="mx-auto max-w-4xl px-6 py-12 lg:px-8">
        <FrameworkChart data={frameworks} />
      </section>

      {/* ════════════════ FRONTEND ════════════════ */}
      <section id="frontend" className="mx-auto max-w-7xl px-6 py-12 lg:px-8 scroll-mt-8">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#3B82F6' }} />
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-gray-400 dark:text-gray-500">
              8 Framework
            </p>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Frontend
          </h2>
        </div>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {frontendFrameworks.map((fw) => (
            <InfographicCard key={fw.framework} data={fw} maxScore={maxScore} maxStars={maxStars} maxDownloads={maxDownloads} accentColor="#3B82F6" />
          ))}
        </div>
      </section>

      {/* ════════════════ BACKEND ════════════════ */}
      <section id="backend" className="mx-auto max-w-7xl px-6 py-12 lg:px-8 scroll-mt-8">
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-2 h-2 rounded-full" style={{ backgroundColor: '#14B8A6' }} />
            <p className="text-xs font-medium uppercase tracking-[0.2em] text-gray-400 dark:text-gray-500">
              10 Framework
            </p>
          </div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Backend
          </h2>
        </div>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {backendFrameworks.map((fw) => (
            <InfographicCard key={fw.framework} data={fw} maxScore={maxScore} maxStars={maxStars} maxDownloads={maxDownloads} accentColor="#14B8A6" />
          ))}
        </div>
      </section>

      {/* ════════════════ RECOMMENDATION ════════════════ */}
      <section className="mx-auto max-w-7xl px-6 py-12 lg:px-8">
        <div className="rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50 p-8 sm:p-10">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
            Rekomendasi Framework per Jenis Project
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-8 max-w-2xl">
            Panduan memilih stack frontend + backend berdasarkan skala dan tipe project.
          </p>

          <div className="space-y-8">
            {/* ── PROJECT KECIL ── */}
            <RecGroup
              title="Project Kecil"
              subtitle="1-2 orang · cepat selesai · budget minim"
              color="#3B82F6"
              items={[
                { title: "Bikin Website / Landing Page", stack: "Astro + Laravel", body: "Zero-JS default, build kilat. Cocok company profile, blog, portfolio. Astro island, Laravel backend full-featured." },
                { title: "Bot / AI Tool", stack: "React + FastAPI", body: "FastAPI async inference, auto-docs. React dashboard ringan untuk monitoring model & hasil prediksi." },
                { title: "Prototype / MVP", stack: "Svelte + Flask", body: "Kurva belajar rendah, setup minimal. Validasi ide dalam hitungan hari tanpa overhead arsitektur." },
              ]}
            />

            {/* ── PROJECT SEDANG ── */}
            <RecGroup
              title="Project Sedang"
              subtitle="3-8 orang · beberapa bulan · perlu scalable"
              color="#14B8A6"
              items={[
                { title: "SaaS Startup", stack: "Next.js + NestJS", body: "SSR & API Routes bawaan, arsitektur modular NestJS. Siap growth dari ratusan ke ribuan user." },
                { title: "E-commerce / Toko Online", stack: "Vue.js + Laravel", body: "Vue reaktif + Laravel ecosystem (Cashier, Scout, Horizon). Payment gateway & inventory out-of-the-box." },
                { title: "Company Internal App", stack: "React + Express.js", body: "Ekosistem React terbesar, Express simpel & fleksibel. Cepat integrasi database & auth internal." },
              ]}
            />

            {/* ── PROJECT BESAR ── */}
            <RecGroup
              title="Project Besar"
              subtitle="10+ orang · multi-tahun · compliance & maintainability"
              color="#F59E0B"
              items={[
                { title: "Enterprise Platform", stack: "Angular + Spring Boot", body: "Opinionated structure, type-safety ketat, dukungan jangka panjang. Cocok banking, healthcare, government." },
                { title: "Marketplace / Multi-tenant", stack: "Next.js + ASP.NET Core", body: "SSR untuk SEO marketplace, .NET performa tinggi, dependency injection, mature ORM (EF Core)." },
                { title: "Real-time / Chat App", stack: "React + Phoenix", body: "Phoenix Channels fault-tolerant, WebSocket native, horizontal scaling. React UI real-time dashboard." },
              ]}
            />
          </div>
        </div>
      </section>

      {/* ════════════════ FOOTER ════════════════ */}
      <footer className="border-t border-gray-100 dark:border-gray-800/50 mt-8">
        <div className="mx-auto max-w-7xl px-6 py-6 lg:px-8">
          <p className="text-center text-xs text-gray-400 dark:text-gray-500">
            Framework Trends Tracker 2026 — GitHub, NPM, PyPI APIs &amp; Stack Overflow Developer Survey 2025
          </p>
        </div>
      </footer>
    </main>
  );
}
