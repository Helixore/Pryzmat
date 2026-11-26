# Patch 00 - initial frontend

- Vite + React + react-router-dom skeleton
- API layer (src/api): endpoints.js, client.js (Token auth)
- Auth (src/auth): AuthContext, ProtectedRoute, roles.js
- Pages: Login, Home, StudentClass list (teacher/principal only)
- backend-patch/pryzmat_auth_token.py: login response now includes `role`

Deleted files: none
Needs `npm install`: yes
