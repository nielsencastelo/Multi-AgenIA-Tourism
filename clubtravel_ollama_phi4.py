#!/usr/bin/env python
# clubtravel_ollama_phi4.py
import os, json, requests
from typing import List, Dict

OLLAMA_ENDPOINT = os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434")
MODEL_NAME = os.environ.get("OLLAMA_MODEL", "phi4")

SYSTEM_PROMPT_EN = (
    "You are DomusMind for Club Travel (Ireland): a helpful travel-operations assistant. "
    "Behave like a senior travel consultant + ops analyst. "
    "Be precise, structured, brief when appropriate, and justify key recommendations. "
    "If you make assumptions, state them. "
    "Never fabricate prices or availability; instead, outline steps to verify. "
    "When giving itineraries, prefer Dublin-centric examples first when relevant to Irish customers. "
    "Use bullet points for lists; otherwise keep paragraphs short. "
)

SYSTEM_PROMPT_PT = (
    "Você é o DomusMind para a Club Travel (Irlanda): um assistente de operações de viagens. "
    "Comporte-se como um consultor sênior de viagens + analista de operações. "
    "Seja preciso, estruturado, breve quando apropriado e justifique recomendações importantes. "
    "Se fizer suposições, explicite-as. "
    "Nunca invente preços ou disponibilidade; em vez disso, descreva como verificar. "
    "Ao sugerir roteiros, prefira exemplos centrados em Dublin quando relevante para clientes irlandeses. "
    "Use marcadores para listas; caso contrário, mantenha parágrafos curtos. "
)

PROMPTS = {
    "itinerary_planner": {
        "en": (
            "Task: Build a 5-day personalized itinerary for {traveler_profile} visiting {destination} in {month}.\\n"
            "Constraints: budget={budget}, interests={interests}.\\n"
            "Deliver: a day-by-day plan (morning/afternoon/evening), logistics hints, and backup options.\\n"
            "Assumptions: state any assumptions you make.\\n"
            "Safety: do not invent prices; list how to verify costs and availability."
        ),
        "pt": (
            "Tarefa: Monte um roteiro personalizado de 5 dias para {traveler_profile} visitando {destination} em {month}.\\n"
            "Restrições: orçamento={budget}, interesses={interests}.\\n"
            "Entregáveis: plano dia a dia (manhã/tarde/noite), dicas de logística e opções de backup.\\n"
            "Suposições: explicite quaisquer suposições feitas.\\n"
            "Segurança: não invente preços; informe como verificar custos e disponibilidade."
        ),
    }
}

def build_messages(system_en: str, user_prompt_en: str, system_pt: str) -> List[Dict[str, str]]:
    system_full = system_en + "\\n\\n[PT-BR translation]\\n" + system_pt
    return [{"role": "system", "content": system_full},
            {"role": "user", "content": user_prompt_en}]

def chat(user_prompt_en: str) -> str:
    url = OLLAMA_ENDPOINT.rstrip("/") + "/api/chat"
    messages = build_messages(SYSTEM_PROMPT_EN, user_prompt_en, SYSTEM_PROMPT_PT)
    r = requests.post(url, json={"model": MODEL_NAME, "messages": messages}, timeout=120)
    r.raise_for_status()
    data = r.json()
    if "message" in data and "content" in data["message"]:
        return data["message"]["content"]
    return data.get("response", str(data))

if __name__ == "__main__":
    prompt = PROMPTS["itinerary_planner"]["en"].format(
        traveler_profile="a couple in their 30s from Dublin",
        destination="Lisbon",
        month="September",
        budget="€1500",
        interests="food markets, historic neighborhoods, scenic viewpoints"
    )
    print(chat(prompt))
