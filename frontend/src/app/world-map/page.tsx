"use client"

import dynamic from "next/dynamic"

// Import WorldMap dynamically to avoid SSR issues with Leaflet
const WorldMap = dynamic(() => import("@/components/world-map"), {
  ssr: false,
  loading: () => (
    <div className="w-full h-[600px] bg-muted animate-pulse rounded-xl flex items-center justify-center">
      <span className="text-neutral-gray">Preparing map components...</span>
    </div>
  ),
})

const MOCK_MAP_DATA: Record<string, number> = {
  USA: 25.4,
  FRA: 2.8,
  CHN: 17.9,
  BRA: 1.9,
  CIV: 0.07,
  DEU: 4.1,
  JPN: 4.2,
  GBR: 3.1,
  IND: 3.4,
  CAN: 2.1,
}

export default function WorldMapPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight">Global Map Explorer</h1>
        <p className="text-neutral-gray text-lg">
          Visualize key indicators across the globe with interactive choropleth maps.
        </p>
      </div>

      <div className="grid gap-6">
        <div className="flex flex-wrap items-center gap-4 bg-card p-4 rounded-lg border shadow-sm">
          <div className="space-y-1">
            <span className="text-xs font-semibold uppercase text-neutral-gray">Indicator</span>
            <div className="font-medium">GDP (current US$ trillion)</div>
          </div>
          <div className="h-10 w-[1px] bg-border mx-2 hidden sm:block" />
          <div className="space-y-1">
            <span className="text-xs font-semibold uppercase text-neutral-gray">Year</span>
            <div className="font-medium">2022</div>
          </div>
        </div>

        <WorldMap
          data={MOCK_MAP_DATA}
          indicatorName="GDP"
          year={2022}
        />

        <div className="flex justify-between items-center text-sm text-neutral-gray italic px-2">
          <span>Source: World Bank Data</span>
          <span>Projections for missing regions based on regional averages</span>
        </div>
      </div>
    </div>
  )
}
