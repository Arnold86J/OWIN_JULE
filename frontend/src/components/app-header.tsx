"use client"

import * as React from "react"
import { Search, Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"

import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { SidebarTrigger } from "@/components/ui/sidebar"

export function AppHeader() {
  const { theme, setTheme } = useTheme()
  const [search, setSearch] = React.useState("")

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("Searching for:", search)
    // Here we will eventually connect to the /search API
  }

  return (
    <header className="sticky top-0 z-10 flex h-16 w-full items-center justify-between border-b bg-background px-4">
      <div className="flex items-center gap-4 flex-1">
        <SidebarTrigger />
        <form onSubmit={handleSearch} className="relative w-full max-w-md hidden md:block">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-neutral-gray" />
          <Input
            type="search"
            placeholder="Search indicators (e.g. GDP, Population)..."
            className="pl-9 bg-muted/50 border-none focus-visible:ring-primary-blue"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </form>
      </div>
      <div className="flex items-center gap-2">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
        >
          <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </div>
    </header>
  )
}
