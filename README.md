# Unofficial CBX API

An unofficial API for [CBX](https://cbx.org.br/) (Confederação Brasileira de Xadrez). You can access the [API/DATA here](https://github.com/emerson-proenca/cbx_api?tab=readme-ov-file#apidata-access).
This project uses WebScraping to gather data, [Typer](https://github.com/fastapi/typer) to create a CLI and [Supabase](https://supabase.com/docs/reference/python/) to store Announcements, News, Players, and Tournaments table.

## Project Structure

```text
├── LICENSE
├── project.py
├── README.md
├── requirements.txt
├── scrapers
│   ├── announcements.py
│   ├── base.py
│   ├── __init__.py
│   ├── news.py
│   ├── players.py
│   └── tournaments.py
└── test_project.py
```

## Setup

It is recommended to use a Python virtual environment.

1. Clone the repository.

```bash
git clone https://github.com/emerson-proenca/cbx_api.git
cd cbx_api
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## API/DATA Access

The data is hosted on Supabase. Access is restricted to **SELECT** queries only.

- **SUPABASE_URL**: `https://kvytmiwenglctskexamo.supabase.co`
- **SUPABASE_KEY**: `sb_publishable_exdFbFdSw2pH_RKSgrEfkQ_6TMPoDax`

## License

This project is licensed under the MIT License.

## Status

This project is currently active and under development.
