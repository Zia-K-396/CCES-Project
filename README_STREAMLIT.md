# Community Energy Management System — Streamlit Demo

Interactive browser demo for the 5-neighbourhood rooftop-solar + Li-ion + CCES concept.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push `app.py` and `requirements.txt` to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app.
4. Select your GitHub repository and branch (`main`).
5. Set the main file to `app.py`.
6. Deploy.

The resulting URL can be shared with judges.

## Demo model

- 5 neighbourhoods
- 4,000 consumer connections per neighbourhood
- 20,000 connections total
- 80 MWh central CCES
- 4 MWh Li-ion at each neighbourhood
- Li-ion initial SOC: randomly 70–95%
- Rooftop PV capacity: 28 MW
- CCES-ground PV capacity: 12 MW
- Local solar serves local demand first
- Excess solar charges local Li-ion, then CCES
- During shortage, local Li-ion responds first
- If a neighbourhood remains short, another neighbourhood's Li-ion can provide support
- Remaining shortage is supplied by CCES
