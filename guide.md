1. **Schedule**: Enable the `pg_cron` and `pg_net` extensions in Supabase to schedule an automated task every 6 hours.
2. **Trigger**: Supabase sends an HTTP POST request via `net.http_post` to your Vercel-hosted Python endpoint.
3. **Scrape**: The Python script on Vercel receives the request, executes the scraping logic, and collects the data.
4. **Update**: Python uses the `supabase-py` SDK to securely insert or update the scraped data directly into your database.
5. **Confirm**: The Python function returns a 200 OK status to Supabase to confirm the scheduled task was successful.


Basicamente o Supabase vai ter um CRON para cada 24h
Isso vai enviar para o Vercel com FastAPI
FastAPI vai responder que recebeu o request, schedule
Scraper começa a fazer o trabalho
Depois salva os dados localmente e envia para o Supabase
