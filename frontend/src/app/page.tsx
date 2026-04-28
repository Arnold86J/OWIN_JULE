export default function Home() {
  return (
    <div className="space-y-6">
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
    </div>
  )
}
