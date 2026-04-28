"use client"

import React from "react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"
import { formatCompactNumber, formatFullNumber } from "@/lib/formatters"

interface TimeLineChartProps {
  data: any[]
  series: {
    key: string
    name: string
    color?: string
  }[]
  showDots?: boolean
  height?: number | string
}

const DEFAULT_COLORS = [
  "var(--primary-blue)",
  "#10b981", // success-green
  "#f59e0b", // amber
  "#6366f1", // indigo
  "#ec4899", // pink
  "#8b5cf6", // violet
]

export function TimeLineChart({
  data,
  series,
  showDots = false,
  height = 400,
}: TimeLineChartProps) {
  const [isMounted, setIsMounted] = React.useState(false)

  React.useEffect(() => {
    setIsMounted(true)
  }, [])

  if (!isMounted) {
    return <div style={{ height }} className="w-full bg-muted/20 animate-pulse rounded-lg" />
  }

  return (
    <div className="w-full" style={{ height }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={data}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="var(--neutral-gray)" opacity={0.2} />
          <XAxis
            dataKey="year"
            axisLine={false}
            tickLine={false}
            tick={{ fill: "var(--neutral-gray)", fontSize: 12 }}
            dy={10}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{ fill: "var(--neutral-gray)", fontSize: 12 }}
            tickFormatter={formatCompactNumber}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "var(--background)",
              border: "1px border var(--neutral-gray)",
              borderRadius: "8px",
              fontSize: "12px"
            }}
            formatter={(value: any) => [formatFullNumber(Number(value)), ""]}
            labelStyle={{ fontWeight: "bold", marginBottom: "4px" }}
          />
          <Legend
            verticalAlign="top"
            align="right"
            height={36}
            iconType="circle"
          />
          {series.map((s, index) => (
            <Line
              key={s.key}
              type="monotone"
              dataKey={s.key}
              name={s.name}
              stroke={s.color || DEFAULT_COLORS[index % DEFAULT_COLORS.length]}
              strokeWidth={2}
              dot={showDots}
              activeDot={{ r: 6, strokeWidth: 0 }}
              isAnimationActive={false}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
