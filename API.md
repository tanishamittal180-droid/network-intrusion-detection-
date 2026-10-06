# API Quick Reference

| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/flows | Validate and analyze one flow |
| GET | /api/flows | List stored flows |
| GET | /api/flows/{id} | Retrieve a flow |
| GET | /api/alerts | List/filter alerts |
| GET | /api/alerts/{id} | Alert plus analyst notes |
| PUT | /api/alerts/{id}/status | Change NEW/INVESTIGATING/RESOLVED/FALSE_POSITIVE |
| POST | /api/alerts/{id}/notes | Add an analyst note |
| GET | /api/dashboard/stats | KPI cards |
| GET | /api/dashboard/traffic | Traffic timeline |
| GET | /api/dashboard/alerts | Severity/type/protocol aggregates |
| GET | /api/rules | Configured rule metadata |

Production requirements should add authentication, authorization, HTTPS, rate limiting, audit logging, and strict CORS.
