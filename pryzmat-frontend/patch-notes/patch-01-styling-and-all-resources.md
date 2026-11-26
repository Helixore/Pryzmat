# Patch 01 - styling + all 14 resource screens

## What's new
- Global stylesheet (light + dark, follows the OS setting), sidebar layout, styled login
- One generic, config-driven list screen used for every endpoint:
  search, click-to-sort headers, detail popup (all fields), refresh,
  loading / empty / error / "no access" states, nice formatting for
  dates, booleans, nested objects and lists
- src/api/resources.js: single config for all 14 resources
  (label, route, group, which roles see it, optional fixed columns)
- Home page now shows tiles for the sections your role can open

## New files
- src/styles/global.css
- src/utils/format.js
- src/api/resources.js
- src/components/Cell.jsx
- src/components/DataTable.jsx
- src/components/DetailModal.jsx
- src/components/StateMessage.jsx
- src/pages/ResourceListPage.jsx

## Changed files
- src/main.jsx            (imports the stylesheet)
- src/App.jsx             (routes generated from resources.js)
- src/auth/roles.js       (NAV_ITEMS removed; now lives in resources.js)
- src/components/Layout.jsx
- src/pages/HomePage.jsx
- src/pages/LoginPage.jsx

## DELETE by hand
- src/pages/StudentClassListPage.jsx   (replaced by ResourceListPage)

## Needs `npm install`: no
## Needs dev server restart: no (Vite hot-reloads), but a restart doesn't hurt
