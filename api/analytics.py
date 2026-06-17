from typing import List, Dict, Any
from decimal import Decimal

def calculate_stats(data_points: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculates min, max, and total growth from data points."""
    if not data_points:
        return {}

    # Sort data by year to ensure correct growth calculation
    sorted_data = sorted(data_points, key=lambda x: x["year"])
    values = [float(x["value"]) for x in sorted_data]
    years = [x["year"] for x in sorted_data]

    v_min = min(values)
    v_max = max(values)

    first_val = values[0]
    last_val = values[-1]

    total_growth = ((last_val - first_val) / first_val * 100) if first_val != 0 else 0

    return {
        "min": v_min,
        "max": v_max,
        "total_growth": round(total_growth, 2),
        "start_year": years[0],
        "end_year": years[-1],
        "start_value": first_val,
        "last_value": last_val
    }

def generate_ai_analysis_prompt(
    indicator_name: str,
    unit: str,
    location: str,
    data_points: List[Dict[str, Any]]
) -> Dict[str, str]:
    """Generates a structured prompt for an LLM to analyze the data trend."""
    stats = calculate_stats(data_points)

    if not stats:
        return {
            "system_prompt": "You are a data journalist.",
            "user_prompt": "No data available for analysis."
        }

    system_prompt = (
        "You are a professional Data Journalist specializing in global trends. "
        "Your goal is to provide a factual, rigorous, and engaging analysis of data trends. "
        "Your summary must be in French, identifying key milestones and significant variations."
    )

    user_prompt = (
        f"Analysez l'indicateur suivant : {indicator_name} ({unit}) pour {location}. "
        f"La période d'analyse s'étend de {stats['start_year']} à {stats['end_year']}.\n\n"
        f"Statistiques clés :\n"
        f"- Valeur initiale : {stats['start_value']} {unit}\n"
        f"- Valeur finale : {stats['last_value']} {unit}\n"
        f"- Croissance totale sur la période : {stats['total_growth']}%\n"
        f"- Minimum atteint : {stats['min']} {unit}\n"
        f"- Maximum atteint : {stats['max']} {unit}\n\n"
        f"Veuillez rédiger un court résumé (environ 150 mots) en français expliquant la tendance observée, "
        f"les points de bascule éventuels et l'importance de cette évolution pour {location}."
    )

    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt
    }
