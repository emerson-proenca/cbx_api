# Unofficial CBX API

An unofficial API for [CBX](https://cbx.org.br/) (Confederação Brasileira de Xadrez). You can access the API/DATA [here](https://github.com/emerson-proenca/cbx_api?tab=readme-ov-file#apidata-access). 

This project uses WebScraping to gather data, [Typer](https://github.com/fastapi/typer) to create a CLI, [Supabase](https://supabase.com/docs/reference/python/) to store Announcements, News, Players, and Tournaments table. With over 100k rows! This project is active and under development, License is MIT, if you like this project you might like [OTB](https://github.com/emerson-proenca/OTB).

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

## API/Data Access

The data is hosted on Supabase. Access is restricted to **SELECT** queries only.

- **SUPABASE_URL**: `https://kvytmiwenglctskexamo.supabase.co`
- **SUPABASE_KEY**: `sb_publishable_exdFbFdSw2pH_RKSgrEfkQ_6TMPoDax`

You can query the data either by using the [Supabase CLI](https://supabase.com/docs/guides/local-development/cli/getting-started) (reccomended), or using the following command:
```bash
python project.py fetch [OPTIONS] TABLE
# Example usage:
python project.py fetch news --select title 
```

## License

The source code of this project is licensed under the [MIT License](https://github.com/emerson-proenca/cbx_api?tab=MIT-1-ov-file).

## Status

This project is currently active and under development.
