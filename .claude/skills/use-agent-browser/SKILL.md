---
name: use-agent-browser
description: Use agent-browser to visually smoke test the Vitals UI after making changes. Verifies routing, rendering, and data display end-to-end beyond what a build check catches.
---

# agent-browser

Browser automation CLI designed for AI agents. Compact text output (~200-400 tokens vs 3000-5000 for raw DOM). Elements get short refs (`@e1`, `@e2`) for deterministic interaction.

## Setup

```bash
agent-browser install   # first-time Chromium setup
```

**Known issue**: agent-browser may look for a specific Chromium version that differs from what's installed. If you get a "Executable doesn't exist" error:

```bash
# Check what's installed
ls ~/Library/Caches/ms-playwright/

# Symlink the installed version to the expected one (adjust version numbers)
ln -sf ~/Library/Caches/ms-playwright/chromium_headless_shell-1217 \
       ~/Library/Caches/ms-playwright/chromium_headless_shell-1208
```

## Basic workflow

Every session follows the same cycle:

```bash
agent-browser open <url>       # 1. navigate
agent-browser snapshot -i      # 2. discover interactive elements
agent-browser click @e1        # 3. interact using refs
agent-browser snapshot -i      # 4. re-snapshot (refs change after navigation/DOM updates)
agent-browser close            # 5. end session
```

## Running Vitals locally

Port 3000 is taken by the trekker dashboard. Always use 3001:

```bash
# In one terminal
cd ~/Repos/ooloth/vitals
npm run dev -- --port 3001

# Then use agent-browser
agent-browser open http://localhost:3001
```

## Key commands

### Navigation
```bash
agent-browser open <url>
agent-browser goto <url>          # same as open
```

### Snapshots
```bash
agent-browser snapshot            # full accessibility tree
agent-browser snapshot -i         # interactive elements only (preferred)
agent-browser snapshot -c         # compact, removes empty elements
agent-browser snapshot -d 3       # limit depth
agent-browser snapshot -s "main"  # scope to CSS selector
```

### Interaction
```bash
agent-browser click @e1
agent-browser fill @e1 "text"     # clear + type
agent-browser type @e1 "text"     # type into focused element
agent-browser press Enter
agent-browser hover @e1
agent-browser scroll down 300
```

### Reading content
```bash
agent-browser get text @e1
agent-browser get attr @e1 href
agent-browser get title
agent-browser get url
```

### Waiting
```bash
agent-browser wait @e1                    # wait for element
agent-browser wait --text "Loaded"        # wait for text
agent-browser wait --load networkidle     # wait for network quiet
agent-browser wait 1000                   # wait N ms
```

### Screenshots
```bash
agent-browser screenshot                  # viewport
agent-browser screenshot --full           # full page
agent-browser screenshot --annotate       # add numbered element labels
agent-browser screenshot /tmp/vitals.png  # save to path
```

## What to verify in Vitals

After UI changes, check:

1. **Sidebar renders** — project names and panel links appear
2. **Active state** — correct link is highlighted on each route
3. **Panel pages load** — navigate to `/projects/[id]/[panel]` and confirm content renders
4. **Data displays** — once real data is wired, confirm tables/lists populate

Example smoke test:

```bash
agent-browser open http://localhost:3001
agent-browser snapshot -i
# expect: sidebar with project groups and panel links

agent-browser click @e1          # click first panel link
agent-browser snapshot -i
# expect: panel heading, project ID shown, data or placeholder visible
```

## Selector types

```bash
@e1                              # ref from snapshot (preferred)
#submit                          # CSS selector
.sidebar-link                    # CSS class
button                           # tag name
find role button --name "Submit" # ARIA role + name
find text "Errors"               # visible text
```

## Sessions

Run multiple isolated browser sessions in parallel:

```bash
agent-browser --session work open http://localhost:3001
agent-browser --session personal open http://localhost:3002
```

## Options

```bash
--headed                         # show browser window (useful for debugging)
--json                           # structured output for scripting
--debug                          # verbose logging
```
