GAAH Bookkeeping — Render-ready package

1) Push this project to a GitHub repository (branch 'main').
2) On Render.com -> New -> Blueprint, connect your repo and deploy.
   Render will create a PostgreSQL database named 'gaah-db' and set DATABASE_URL automatically.
3) Admin credentials (pre-seeded):
   - username: admin
   - password: admin123
4) After deployment, open the URL provided by Render and log in.
5) To change secret keys or settings, set environment variables in Render:
   - SECRET_KEY
   - DATABASE_URL (provided by Render when it creates the DB)
