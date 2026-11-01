# Study Planner API — Lab 12 Part 05

This project extends the Lab 11 FastAPI app with a PostgreSQL service. The
Compose project name is `lab12-project-studyplanner-<STUDENT_ID>`, separate
from both the reference stack and the earlier Lab 11 folder. The app is
published on `localhost:8085` by default; it connects to PostgreSQL using the
Compose service hostname `db`.

## Start the stack

In PowerShell, from this folder:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Edit `.env` with your student ID and disposable local database credentials,
then run. If the default host port `8085` is already in use, set `APP_PORT` to
an available port; this machine uses `8087`:

```powershell
docker compose config --quiet
docker compose up -d --build --wait
docker compose ps
curl.exe http://localhost:8085/health
curl.exe http://localhost:8085/today
```

The database health check gates app startup, and the app health check runs a
database query. The database is not published to the host.

## Create and read a student record

Replace the example ID and goal with your own:

```powershell
$session = @{
    student_id = '6788185'
    subject = 'Databases'
    goal = 'Lab12-6788185-own-project-proof'
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri 'http://localhost:8085/sessions' `
    -ContentType 'application/json' -Body $session
Invoke-RestMethod -Uri 'http://localhost:8085/sessions' | ConvertTo-Json -Depth 5
docker compose exec -T db psql -U studyplanner -d studyplanner `
    -c "SELECT id, student_id, subject, goal, created_at FROM study_sessions;"
```

Save the returned ID, goal, and `created_at`; use this same record for the
persistence checks without posting it again.

## Prove persistence

Record the DB container ID and mounted named volume before testing:

```powershell
$dbBefore = docker compose ps -q db
$dbBefore
docker inspect --format "{{json .Mounts}}" $dbBefore
```

Restart and read the record again:

```powershell
docker compose restart
docker compose up -d --wait
Invoke-RestMethod -Uri 'http://localhost:8085/sessions' | ConvertTo-Json -Depth 5
```

Remove and recreate the containers without deleting the named volume:

```powershell
docker compose down
docker compose up -d --wait
$dbAfter = docker compose ps -q db
$dbAfter
docker inspect --format "{{json .Mounts}}" $dbAfter
Invoke-RestMethod -Uri 'http://localhost:8085/sessions' | ConvertTo-Json -Depth 5
docker compose exec -T db psql -U studyplanner -d studyplanner `
    -c "SELECT id, student_id, subject, goal, created_at FROM study_sessions;"
```

The DB container ID should change after `down/up`; the named volume and
original session ID, goal, and creation time should remain unchanged. The
volume stores data outside the disposable container, but it is not a backup.
For normal cleanup, use `docker compose down` without `-v` and retain the
volume until your evidence is complete.
