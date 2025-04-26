
import pandas as pd

# Load and normalize datasets
def load_datasets():
    file_paths = {
        "comfort_speaking": "data/perceived-comfort-speaking-anxiety-depression.csv",
        "mental_health_policy": "data/stand-alone-policy-or-plan-for-mental-health.csv",
        "gov_funding_support": "data/share-who-say-its-extremely-important-for-the-national-government-to-fund-research-on-anxietydepression.csv",
        "lifetime_anxiety_depression": "data/share-who-report-lifetime-anxiety-or-depression.csv",
        "science_vs_gdp": "data/science-helps-a-lot-treating-anxiety-depression-vs-gdp-per-capita.csv",
        "schizophrenia_prevalence": "data/schizophrenia-prevalence.csv",
        "schizophrenia_gender": "data/schizophrenia-prevalence-males-vs-females.csv",
        "schizophrenia_age": "data/schizophrenia-prevalence-by-age.csv",
        "psychiatrists_per_country": "data/psychiatrists-working-in-the-mental-health-sector.csv"
    }

    data = {k: pd.read_csv(v) for k, v in file_paths.items()}
    for df in data.values():
        if 'Entity' in df.columns:
            df['Entity'] = df['Entity'].str.strip().str.lower()
    return data

# Utility Functions
def get_comfort_stats(country, df):
    country = country.lower()
    row = df[df["Entity"] == country]
    if not row.empty:
        very = row.iloc[0, 2]
        some = row.iloc[0, 3]
        none = row.iloc[0, 4]
        return f"In {country.title()}, {very:.1f}% feel very comfortable discussing mental health, {some:.1f}% somewhat comfortable, and {none:.1f}% not at all comfortable."
    return "No comfort speaking data available."

def get_policy_status(country, df):
    country = country.lower()
    row = df[df["Entity"] == country]
    if not row.empty:
        status = row.iloc[0, -1]
        return f"{country.title()} has a national mental health policy." if 'yes' in str(status).lower() else f"{country.title()} does not have a national mental health policy."
    return "No policy data available."

def get_research_support(country, df):
    country = country.lower()
    row = df[df["Entity"] == country]
    if not row.empty:
        percent = row.iloc[0, -1]
        return f"{percent:.1f}% of people in {country.title()} think government should fund mental health research."
    return "No data on public research support."

def get_lifetime_disorder_prevalence(country, df):
    country = country.lower()
    row = df[df["Entity"] == country]
    if not row.empty:
        rate = row.iloc[0, -1]
        return f"In {country.title()}, {rate:.1f}% of the population reports having experienced anxiety or depression."
    return "No prevalence data available."

def get_psychiatrist_density(country, df):
    country = country.lower()
    row = df[df["Entity"] == country]
    if not row.empty:
        rate = row.iloc[0, -1]
        return f"{country.title()} has about {rate:.2f} psychiatrists per 100,000 people."
    return "No psychiatrist data available."

# Add more as needed (e.g., schizophrenia by age/gender, science trust)
from chatbot_utils import *
data = load_datasets()
print(get_comfort_stats("India", data["comfort_speaking"]))
