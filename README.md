# Life Abroad

A self-hosted platform for sharing life updates with friends and family back home — built for people living abroad.

Create posts with photos and videos, organize your contacts into **audiences**, and publish to the audiences you choose. Each contact receives an SMS with a personalized link and views the post in their browser — **no account or app install required on their end.**

> Personal full-stack project: React Native mobile app, React web app, and a FastAPI backend. Was self-hosted on a Raspberry Pi behind a Cloudflare Tunnel (no longer deployed).

## How it works

1. **You** sign in (mobile or web) and add contacts.
2. Group contacts into **audiences** (e.g. "Family", "College friends").
3. Create a **post** — text plus photos/videos — and select which audiences see it.
4. Each contact gets an **SMS** containing a unique, signed link.
5. They tap the link and view the post — access is scoped to that contact via a JWT view token, so no login is needed.

## Architecture

Monorepo with three apps and a shared deployment:

```
life-abroad/
├── apps/
│   ├── mobile/      # React Native app (iOS + Android)
│   ├── frontend/    # React + Vite web SPA
│   └── server/      # FastAPI backend (clean architecture)
├── docker-compose.yaml
└── Makefile
```

The backend follows a **clean / hexagonal architecture**, separating concerns into:

- `domain/` — models and business logic (posts, audiences, contacts, media, notifications)
- `infrastructure/` — database, repositories, auth, storage, SMS
- `interfaces/` — HTTP API routes

## Tech stack

| Layer | Technologies |
|-------|--------------|
| **Mobile** | React Native (iOS + Android) |
| **Web** | React, Vite, Tailwind CSS |
| **Backend** | FastAPI, SQLModel, FastAPI-Users (JWT auth) |
| **Database** | PostgreSQL (async via `asyncpg`) |
| **Media storage** | MinIO (S3-compatible object storage) |
| **Notifications** | SMS via Vonage |
| **Auth** | JWT bearer tokens for users; scoped view tokens for shareable links |
| **Infrastructure** | Docker Compose, self-hosted on Raspberry Pi |
| **Networking** | Cloudflare Tunnel (HTTPS, no port forwarding) |
| **CI/CD** | GitHub Actions (test on PR, deploy on merge) |

## Getting started

### Backend

```bash
cp apps/server/.env.example apps/server/.env   # fill in your values
make setup                                      # create venv, install deps
make test                                       # run the test suite
make run                                         # start via Docker Compose
```

The API serves OpenAPI docs at `http://localhost:8000/docs`.

### Web frontend

```bash
cd apps/frontend
npm install
npm run dev
```

### Mobile app

```bash
cd apps/mobile
npm install
npm run ios       # or: npm run android
```

See [`apps/server/README.md`](apps/server/README.md) for backend, deployment, and Cloudflare DNS details.
