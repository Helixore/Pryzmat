# Pryzmat frontend

React + Vite frontend for the Pryzmat Django/DRF backend.

## Run

    npm install
    npm run dev

Django must be running on http://127.0.0.1:8000. Vite proxies `/api` to it
(see vite.config.js), so no CORS setup is needed in development.

## Backend change required

The login response must include `role`. See `backend-patch/pryzmat_auth_token.py`.

## Applying later patches (drag-and-drop)

Patch zips contain only new or changed files, using the same folder layout
as this project. To apply one:

1. Extract the patch zip into the project root and choose "Replace" /
   "Merge" when asked about existing folders and files.
2. Open `patch-notes/patch-XX-*.md` from the patch. It lists any files you
   must DELETE by hand (extracting cannot delete files) and whether you need
   to run `npm install` again.
3. Restart `npm run dev` if the notes say package.json or vite.config.js changed.

Tip: commit to git before applying a patch, so you can see exactly what changed.
