"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { ChevronsUpDown, Check } from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import type { ProjectConfig } from "@/lib/config/schema";

const PANEL_LABELS: Record<string, string> = {
  errors: "Errors",
};

interface Props {
  projects: Pick<ProjectConfig, "id" | "name" | "panels">[];
}

export function AppSidebar({ projects }: Props) {
  const pathname = usePathname();
  const router = useRouter();

  const currentProjectId = pathname.match(/^\/projects\/([^/]+)/)?.[1];
  const currentProject =
    projects.find((p) => p.id === currentProjectId) ?? projects[0];

  function handleProjectSelect(project: (typeof projects)[number]) {
    const firstPanel = project.panels[0];
    if (firstPanel) {
      router.push(`/projects/${project.id}/${firstPanel.type}`);
    }
  }

  return (
    <Sidebar>
      <SidebarHeader>
        <DropdownMenu>
          <DropdownMenuTrigger
            render={
              <SidebarMenuButton className="w-full justify-between" />
            }
          >
            <span className="truncate font-medium">
              {currentProject?.name ?? "Select project"}
            </span>
            <ChevronsUpDown className="ml-auto shrink-0 opacity-50" size={14} />
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="w-[--radix-dropdown-menu-trigger-width]"
            align="start"
          >
            {projects.map((project) => (
              <DropdownMenuItem
                key={project.id}
                onSelect={() => handleProjectSelect(project)}
              >
                <span className="flex-1">{project.name}</span>
                {project.id === currentProject?.id && (
                  <Check size={14} className="ml-2 shrink-0" />
                )}
              </DropdownMenuItem>
            ))}
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarHeader>

      <SidebarContent>
        {currentProject && (
          <SidebarGroup>
            <SidebarGroupLabel>Panels</SidebarGroupLabel>
            <SidebarMenu>
              {currentProject.panels.map((panel) => {
                const href = `/projects/${currentProject.id}/${panel.type}`;
                return (
                  <SidebarMenuItem key={panel.type}>
                    <SidebarMenuButton
                      render={<Link href={href} />}
                      isActive={pathname === href}
                    >
                      {PANEL_LABELS[panel.type] ?? panel.type}
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroup>
        )}
      </SidebarContent>
    </Sidebar>
  );
}
