# Unofficial CBX API

An unofficial API for CBX (Confederação Brasileira de Xadrez). This project uses WebScraping to gather data from https://cbx.org.br/ and Supabase to store data regarding announcements, news, players, and tournaments.

## Project Structure

```text
├── cbx
│   ├── __init__.py
│   ├── announcements.py
│   ├── base.py
│   ├── news.py
│   ├── players.py
│   └── tournaments.py
├── LICENSE
├── README.md
├── requirements.txt
└── supabase.sql
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

## Database Access

The data is hosted on Supabase. Access is restricted to **SELECT** queries only.

- **SUPABASE_URL**: `https://kvytmiwenglctskexamo.supabase.co`
- **SUPABASE_KEY**: `sb_publishable_exdFbFdSw2pH_RKSgrEfkQ_6TMPoDax`

## License

This project is licensed under the MIT License.

## Status

This project is currently active and under development.
