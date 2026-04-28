import { Metadata } from "next"
import { notFound } from "next/navigation"
import { TimeLineChart } from "@/components/charts/lazy-chart"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function getIndicator(code: string) {
  // Try to fetch from API, fallback to mock if API is down during build
  try {
    const res = await fetch(`${API_BASE_URL}/search?q=${code}&limit=1`, {
      next: { revalidate: 3600 }
    })
    if (!res.ok) return null
    const data = await res.json()
    return data.items.find((i: any) => i.code === code) || null
  } catch (e) {
    // Fallback for popular indicators during build if API is unreachable
    const fallbacks: Record<string, any> = {
      "NY.GDP.MKTP.CD": { name: "GDP (current US$)", unit: "USD", code: "NY.GDP.MKTP.CD" },
      "SP.POP.TOTL": { name: "Population, total", unit: "Count", code: "SP.POP.TOTL" },
      "SP.DYN.LE00.IN": { name: "Life expectancy at birth", unit: "Years", code: "SP.DYN.LE00.IN" }
    }
    return fallbacks[code] || null
  }
}

export async function generateMetadata({ params }: { params: { code: string } }): Promise<Metadata> {
  const { code } = await params
  const indicator = await getIndicator(code)

  if (!indicator) return { title: "Indicator Not Found" }

  return {
    title: `${indicator.name} Evolution & Analysis | World Data Insight`,
    description: `Detailed historical evolution and data analysis for ${indicator.name}. Global trends from 1960 to 2023.`,
    openGraph: {
      title: `${indicator.name} - World Data Trends`,
      description: `Explore ${indicator.name} across countries with interactive visualizations.`,
    }
  }
}

export async function generateStaticParams() {
  return [
    { code: "NY.GDP.MKTP.CD" },
    { code: "SP.POP.TOTL" },
    { code: "SP.DYN.LE00.IN" }
  ]
}

export default async function IndicatorPage({ params }: { params: { code: string } }) {
  const { code } = await params
  const indicator = await getIndicator(code)

  if (!indicator) {
    notFound()
  }

  // Mock data for the chart if real data fetching is not yet fully implemented for single series
  const MOCK_DATA = [
    { year: 2010, value: 66 },
    { year: 2015, value: 72 },
    { year: 2020, value: 78 },
    { year: 2023, value: 85 },
  ]

  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight text-primary-blue dark:text-foreground">
          {indicator.name}
        </h1>
        <p className="text-neutral-gray text-lg max-w-3xl italic">
          Indicateur : <span className="font-mono">{indicator.code}</span> | Unité : {indicator.unit || "unité"}
        </p>
      </div>

      <div className="p-6 rounded-xl border bg-card shadow-sm space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Tendances Mondiales</h2>
          <span className="text-sm text-neutral-gray">Dernière mise à jour : {new Date().getFullYear()}</span>
        </div>

        <TimeLineChart
          data={MOCK_DATA}
          series={[{ key: "value", name: indicator.name }]}
        />
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="p-6 rounded-xl border bg-card shadow-sm md:col-span-2">
          <h3 className="font-semibold text-lg mb-3">Analyse & Contexte</h3>
          <p className="text-neutral-gray leading-relaxed">
            {indicator.description || "Cet indicateur est essentiel pour comprendre les dynamiques macro-économiques et sociales à l'échelle mondiale. Notre plateforme utilise des données vérifiées de la Banque Mondiale pour assurer une analyse rigoureuse."}
          </p>
        </div>
        <div className="p-6 rounded-xl border bg-card shadow-sm">
          <h3 className="font-semibold text-lg mb-3">Données</h3>
          <ul className="space-y-2 text-sm text-neutral-gray">
            <li className="flex justify-between"><span>Couverture</span> <span className="font-medium text-foreground">Mondiale</span></li>
            <li className="flex justify-between"><span>Période</span> <span className="font-medium text-foreground">1960 - 2023</span></li>
            <li className="flex justify-between"><span>Source</span> <span className="font-medium text-foreground">World Bank</span></li>
          </ul>
        </div>
      </div>
    </div>
  )
}
