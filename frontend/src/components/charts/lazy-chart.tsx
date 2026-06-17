"use client"

import dynamic from "next/dynamic"

export const TimeLineChart = dynamic(
  () => import("./time-line-chart").then(mod => mod.TimeLineChart),
  {
    ssr: false,
    loading: () => <div className="h-[400px] w-full bg-muted animate-pulse rounded-xl" />
  }
)
