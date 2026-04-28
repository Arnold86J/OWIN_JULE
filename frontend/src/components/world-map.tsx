"use client"

import React, { useEffect, useState, useMemo } from "react"
import { MapContainer, GeoJSON, TileLayer } from "react-leaflet"
import "leaflet/dist/leaflet.css"
import * as d3 from "d3-scale"
import * as d3Chromatic from "d3-scale-chromatic"
import { formatCompactNumber } from "@/lib/formatters"
import { useTheme } from "next-themes"

interface WorldMapProps {
  data: Record<string, number> // Map of ISO alpha-3 to value
  indicatorName: string
  year: number
}

const GEOJSON_URL = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"

export default function WorldMap({ data, indicatorName, year }: WorldMapProps) {
  const [geoJson, setGeoJson] = useState<any>(null)
  const { theme } = useTheme()

  useEffect(() => {
    fetch(GEOJSON_URL)
      .then(res => res.json())
      .then(setGeoJson)
  }, [])

  const colorScale = useMemo(() => {
    const values = Object.values(data)
    const min = Math.min(...values)
    const max = Math.max(...values)

    return d3.scaleSequential(d3Chromatic.interpolateBlues)
      .domain([min, max])
  }, [data])

  const onEachCountry = (feature: any, layer: any) => {
    const isoCode = feature.properties.ISO_A3
    const value = data[isoCode]
    const countryName = feature.properties.ADMIN

    layer.on({
      mouseover: (e: any) => {
        const l = e.target
        l.setStyle({
          weight: 2,
          color: "var(--primary-blue)",
          fillOpacity: 0.9,
        })
      },
      mouseout: (e: any) => {
        const l = e.target
        l.setStyle({
          weight: 0.5,
          color: theme === "dark" ? "#333" : "#fff",
          fillOpacity: 0.7,
        })
      },
    })

    layer.bindTooltip(
      `<div class="p-1 font-sans">
        <div class="font-bold">${countryName}</div>
        <div class="text-xs">${indicatorName}: ${value !== undefined ? formatCompactNumber(value) : "No Data"}</div>
        <div class="text-[10px] text-neutral-gray">${year}</div>
      </div>`,
      { sticky: true, className: "rounded-lg border-none shadow-lg bg-background" }
    )
  }

  const countryStyle = (feature: any) => {
    const isoCode = feature.properties.ISO_A3
    const value = data[isoCode]

    return {
      fillColor: value !== undefined ? colorScale(value) : (theme === "dark" ? "#1e293b" : "#e2e8f0"),
      weight: 0.5,
      opacity: 1,
      color: theme === "dark" ? "#333" : "#fff",
      fillOpacity: 0.7,
    }
  }

  if (!geoJson) {
    return (
      <div className="w-full h-[600px] bg-muted animate-pulse rounded-xl flex items-center justify-center">
        <span className="text-neutral-gray">Loading world map data...</span>
      </div>
    )
  }

  const tileLayerUrl = theme === "dark"
    ? "https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png"
    : "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png"

  return (
    <div className="h-[600px] w-full rounded-xl overflow-hidden border shadow-inner bg-muted/20">
      <MapContainer
        center={[20, 0]}
        zoom={2}
        minZoom={2}
        maxZoom={8}
        scrollWheelZoom={true}
        style={{ height: "100%", width: "100%", background: "transparent" }}
        attributionControl={false}
      >
        <TileLayer url={tileLayerUrl} />
        <GeoJSON
          data={geoJson}
          style={countryStyle}
          onEachFeature={onEachCountry}
        />
      </MapContainer>
    </div>
  )
}
