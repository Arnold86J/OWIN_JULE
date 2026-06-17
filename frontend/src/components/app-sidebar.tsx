"use client"

import * as React from "react"
import {
  BarChart3,
  Globe,
  LayoutDashboard,
  BookOpen,
} from "lucide-react"

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar"

const data = {
  navMain: [
    {
      title: "Navigation",
      items: [
        {
          title: "Dashboard",
          url: "/",
          icon: LayoutDashboard,
        },
        {
          title: "Indicators Explorer",
          url: "/explorer",
          icon: BarChart3,
        },
        {
          title: "World Map",
          url: "/map",
          icon: Globe,
        },
        {
          title: "Data Stories",
          url: "/stories",
          icon: BookOpen,
        },
      ],
    },
  ],
}

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <div className="flex items-center gap-2 px-2 py-4">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary-blue text-white">
            <BarChart3 className="h-5 w-5" />
          </div>
          <span className="font-bold text-lg truncate group-data-[collapsible=icon]:hidden">World Data Insight</span>
        </div>
      </SidebarHeader>
      <SidebarContent>
        {data.navMain.map((group) => (group.items.length > 0 && (
          <SidebarGroup key={group.title}>
            <SidebarGroupLabel>{group.title}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {group.items.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton tooltip={item.title} render={<a href={item.url} />}>
                      <item.icon />
                      <span>{item.title}</span>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        )))}
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  )
}
