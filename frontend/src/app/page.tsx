import { TimeLineChart } from "@/components/charts/time-line-chart"

const MOCK_CHART_DATA = [
  { year: 2010, FRA: 2.6, CIV: 0.02, USA: 14.9 },
  { year: 2012, FRA: 2.7, CIV: 0.03, USA: 16.2 },
  { year: 2014, FRA: 2.8, CIV: 0.04, USA: 17.5 },
  { year: 2016, FRA: 2.5, CIV: 0.05, USA: 18.7 },
  { year: 2018, FRA: 2.8, CIV: 0.07, USA: 20.5 },
  { year: 2020, FRA: 2.6, CIV: 0.08, USA: 21.1 },
  { year: 2022, FRA: 2.8, CIV: 0.10, USA: 25.4 },
]

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight text-primary-blue dark:text-foreground">World Data Insight</h1>
        <p className="text-neutral-gray text-lg">
          Explore global trends in economy, health, environment, and demographics.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {[
          { label: "Total Countries", value: "217", color: "primary-blue" },
          { label: "Active Indicators", value: "1,450", color: "success-green" },
          { label: "Data Points", value: "4.2M", color: "neutral-gray" },
          { label: "Updates Today", value: "12", color: "danger-red" },
        ].map((stat) => (
          <div
            key={stat.label}
            className="p-6 rounded-xl border bg-card shadow-sm"
          >
            <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
            <p className="text-2xl font-bold mt-1" style={{ color: `var(--${stat.color})` }}>
              {stat.value}
            </p>
          </div>
        ))}
      </div>

      <div className="p-6 rounded-xl border bg-card shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">GDP Growth Comparison (Trillions USD)</h2>
        </div>
        <TimeLineChart
          data={MOCK_CHART_DATA}
          series={[
            { key: "USA", name: "United States" },
            { key: "FRA", name: "France" },
            { key: "CIV", name: "Côte d'Ivoire" },
          ]}
        />
      </div>
    </div>
  )
}
