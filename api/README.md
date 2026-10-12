# Inst Call API

Local Django API for Inst Call. The project requires Python 3.12 or later and PostgreSQL.

## Prerequisites

- Python 3.12+
- PostgreSQL running locally

On macOS, Python 3.12 can be installed with Homebrew:

```bash
brew update
brew install python@3.12
```

Confirm the installed version:

```bash
python3.12 --version
```

## Set up Python

From this `api` directory, create and activate an isolated virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

`-m` tells Python to run a module as a program. Using `python -m pip` ensures that packages are installed for the same Python interpreter (the active `.venv`).

Install the API dependencies in editable mode:

```bash
python -m pip install -e .
```

Install test/development dependencies as well:

```bash
python -m pip install --group dev
```

To leave the virtual environment later, run `deactivate`.

## Set up PostgreSQL

Check that PostgreSQL is accepting connections:

```bash
pg_isready
```

If PostgreSQL was installed via Homebrew and is not running:

```bash
brew services start postgresql
```

Connect to the default maintenance database:

```bash
psql -d postgres
```

If your macOS user does not have a PostgreSQL role, try:

```bash
psql -U postgres -d postgres
```

At the `psql` prompt, create the local role and database:

```sql
CREATE ROLE inst_call WITH LOGIN PASSWORD 'inst_call';
CREATE DATABASE inst_call OWNER inst_call;
\q
```

Only create each item once. If it already exists, leave it as-is.

## Configure environment variables

The repository root includes an `.env.example` with the expected local settings. Copy it to `.env` once; Django loads that file automatically for `runserver`, migrations, tests, and other management commands.

```bash
cp ../.env.example ../.env
```

Values already set in your shell or deployment environment take precedence over `.env`. Use a strong, unique `DJANGO_SECRET_KEY` outside local development. Google OAuth credentials are only needed to test Google sign-in.

## Run locally

With the virtual environment active, apply database migrations and start the server:

```bash
python manage.py migrate
python manage.py runserver
```

The API runs at <http://127.0.0.1:8000/>. Useful routes include:

- <http://127.0.0.1:8000/admin/>
- <http://127.0.0.1:8000/api/v1/auth/>

To verify the Django configuration without starting the server:

```bash
python manage.py check
```
