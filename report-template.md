# ITCS258 Lab 12 — Compose and persistent data / Compose และข้อมูลถาวร

Student ID / รหัสนักศึกษา: 6788185

Name / ชื่อ: Daranpob Sianghen

Operating system and Docker context / ระบบปฏิบัติการและ Docker context: Windows with Docker Desktop using desktop-linux.

Own project and repository URL / โปรเจกต์และ URL repository:
<https://github.com/boncedy/study-planner-v2>

Complete all five sections with commands, actual output and readable screenshots
from your own screen. Explain in English or Thai. Export `student_ID_lab12.PDF`,
using your actual student ID, for the Lab 12 assignment on MyCourse.

ทำครบทั้งห้าส่วน แสดงคำสั่ง ผลจริง และภาพจากหน้าจอของตนเอง อธิบายภาษาอังกฤษ
หรือไทยได้ ส่งออก `student_ID_lab12.PDF` โดยใช้รหัสนักศึกษาจริง สำหรับงาน Lab 12 บน MyCourse

## 01 · Lab 11 baseline and Compose readiness / ความพร้อมจาก Lab 11

- Docker and Compose versions, Docker context and engine evidence.
- Existing Dockerfile, app command, container port and successful baseline route.
- Which Lab 11 commands/settings become Compose configuration?

Evidence and explanation / หลักฐานและคำอธิบาย:

Lab 11 uses FastAPI (`python:3.12-slim`, `python main.py`, container port
`8000`). The original Git version returned HTTP success from `/health` and
`/today`. Docker Engine is `29.8.2`, Compose is `v5.6.0`, and the context is
`desktop-linux`. Compose replaces `docker run` options with `build`, `ports`,
and `environment`, and adds the database and volume.

## 02 · App + DB stack / แอปและฐานข้อมูล

- Compose definition of the two services and named volume.
- Image major and correct DB volume path.
- Stack startup, healthy service status, logs and DB-aware API health result.
- Which service publishes a host port, and why?

Evidence and explanation / หลักฐานและคำอธิบาย:

The reference stack has `app` and `db`. Express listens on port `3000`;
PostgreSQL 18 stores data in `lab12-express-6788185_pgdata`, mounted at
`/var/lib/postgresql`. Only the app is published (`localhost:8082`); the
database is private to the Compose network. Both services became healthy, and
`/health` reported a connected database.

## 03 · Configuration, networking and data / ค่าตั้งค่า เครือข่าย และข้อมูล

- Sanitized `.env.example` and explicit container environment configuration.
- Draw browser → app and app → DB connections with hostname and port.
- Explain `db` versus app-side `localhost`.
- POST your own student-specific record; capture GET and independent SQL results.
- Record the original row ID, marker and creation time.

Optional testing tool / เครื่องมือทดสอบที่เลือกใช้:
<b>Postman, PowerShell, and curl</b>

For Postman screenshots, show the request method and URL, response status, JSON
and Test Results. For another client, show equivalent request/response evidence.
After restart/down/up, run only the read request; do not create the proof row again.
This guidance adds no required report section or extra task.

หากใช้ Postman ให้ภาพเห็น method, URL, status, JSON และ Test Results
หากใช้เครื่องมืออื่น ให้แสดงคำขอและคำตอบที่เทียบเท่ากัน หลัง restart/down/up
ส่งเฉพาะคำขออ่าน ห้ามเพิ่มแถวหลักฐานใหม่ คำแนะนำนี้ไม่เพิ่มหัวข้อรายงานหรืองานที่ต้องส่ง

Evidence and explanation / หลักฐานและคำอธิบาย:

Compose passes PostgreSQL settings to both containers. The app connects to
`db:5432` (`db` is the service name); the browser connects to
`localhost:8082`. App-side `localhost` would point to the app container itself.

My API and SQL checks showed note ID `4`, marker
`Lab12-6788185-persistence-proof`, created at `2026-11-01T10:44:32.232Z`.
PowerShell/curl is sufficient; Postman is optional.

**Capture:** Sanitized `.env.example`, Compose environment settings, POST and GET
responses, and the matching SQL row. Do not show credentials or POST again
during persistence checks.

## 04 · Persistence after replacement / ข้อมูลหลังสร้างคอนเทนเนอร์ใหม่

| Test | DB container ID (short) | Named volume | Record ID | Marker + created_at |
| --- | --- | --- | --- | --- |
| Initial | `e096b382fd03` | `lab12-express-6788185_pgdata` | 4 | `Lab12-6788185-persistence-proof`; `2026-11-01T10:44:32.232Z` |
| After restart | `e096b382fd03` | `lab12-express-6788185_pgdata` | 4 | `Lab12-6788185-persistence-proof`; `2026-11-01T10:44:32.232Z` |
| After down/up | `e973bc8767dd` | `lab12-express-6788185_pgdata` | 4 | `Lab12-6788185-persistence-proof`; `2026-11-01T10:44:32.232Z` |

- Include actual restart and down/up commands and the subsequent API/SQL results.
- Show the changed DB container ID and unchanged original record without reinsertion.
- Confirm the same named volume remains mounted. Equivalent JSON/SQL timestamp
  formats may differ; compare the represented instant.
- Explain what ordinary `down` retains, what `down -v` removes, and why a volume
  is not a backup. Do not delete your only evidence dataset to answer this question.

Evidence and explanation / หลักฐานและคำอธิบาย:

After restart, the DB kept its container ID. After `down/up`, it changed from
`e096b382…` to `e973bc87…`; the volume remained
`lab12-express-6788185_pgdata`. Note ID `4`, its marker, and timestamp were
unchanged without reinserting it. `down` keeps named volumes; `down -v` removes
them. A volume is not a backup because it can still be lost or damaged.

## 05 · Own project / โปรเจกต์ของตนเอง

Project name, framework and DB engine / ชื่อโปรเจกต์ framework และฐานข้อมูล:
`lab12-project-studyplanner-6788185`; Study Planner API; FastAPI + PostgreSQL 18.

Actual write/read route / route เพิ่มและอ่านข้อมูลจริง:
`POST /sessions` and `GET /sessions`.

Container port and host port / พอร์ตคอนเทนเนอร์และพอร์ตโฮสต์:
Container `8000`; host `8087` (8085–8086 were occupied by other local stacks).

Volume name and target path / ชื่อ volume และตำแหน่งที่ mount:
`lab12-project-studyplanner-6788185_pgdata` → `/var/lib/postgresql`.


- Show your own app + DB Compose configuration and startup instructions.
- Use a stable project/volume identity distinct from the reference stack.
- Show a successful write and read through your actual project API.
- Repeat the container-replacement proof for the project data.
- Explain a problem and fix, or a useful preventive check.
- Explain how this local architecture will map to application and database
  services in Lab 13. Do not claim that local data automatically migrates online.

Evidence and explanation / หลักฐานและคำอธิบาย:

The Lab 12 copy is in its own `Study-Planner-API` folder, separate from the
Lab 11 folder and reference stack. Compose uses its own project and volume.
`POST /sessions` and `GET /sessions` verified session ID `1`,
`Lab12-6788185-own-project-proof`, created at
`2026-11-01T12:27:29.133195Z`. The DB container changed from
`278f10bac420` to `0667c8989b73` after `down/up`; the named volume
`lab12-project-studyplanner-6788185_pgdata` and record stayed the same.

The first copied Compose name would have shared the Lab 11 stack identity.
Giving this Lab 12 copy its own project name created a separate volume. Local
port `8087` was used because `8085` and `8086` were occupied.
This app/database layout maps to Lab 13 services, but local data does not
migrate online automatically.

**Capture:** Healthy services, health response, POST/GET/SQL results, and DB
IDs/mounts before and after `down/up`. After creating the proof record, use
GET only; don’t POST it again.

## Final check / ตรวจสอบก่อนส่ง

- All five sections and both reference/own-project persistence proofs are present.
- Every screenshot is from my own screen and readable in the exported PDF.
- No real passwords or tokens appear in screenshots, source or resolved configuration.
- Repository URL and relevant Compose/configuration changes are included.
- Filename is my actual student ID followed by `_lab12.PDF`.
- The uploaded MyCourse PDF opens and displays correctly.
