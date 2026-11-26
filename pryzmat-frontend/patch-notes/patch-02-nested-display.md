# Patch 02 - readable nested data

Fixes seen in the screenshots:
- Nested objects showed as a bare "Object" badge (e.g. Schedule -> Student class).
  They now get a real label: "2024 A", "Letni · 2024 A", teacher/student names, etc.
- The details popup dumped raw JSON for nested data. It now shows collapsible
  key/value blocks (students list, homeroom teacher, subject -> class -> ...).
- People tables (students, teachers, parents, principals, workers) no longer
  show PESEL/address columns by default; the details popup still has them.

## New files
- src/components/NestedValue.jsx
- src/styles/nested.css

## Changed files
- src/utils/format.js
- src/components/DetailModal.jsx
- src/api/resources.js

## DELETE by hand: none
## Needs `npm install`: no
## Needs dev server restart: no
