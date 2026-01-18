import streamlit as st
import requests
import re
import json
from urllib.parse import urlparse
from bs4 import BeautifulSoup


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="TS4 Mod Analyzer — Phase 1",
    layout="centered"
)

MAX_TEXT_CHARS = 12000


# =========================
# UTILS
# =========================

def detect_source(url: str) -> str:
    domain = urlparse(url).netloc.lower()

    if "patreon.com" in domain:
        return "patreon"
    if "tumblr.com" in domain:
        return "tumblr"
    if "itch.io" in domain:
        return "itch"
    if domain:
        return "website"
    return "unknown"


def fetch_page(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=20)

    if response.status_code == 403:
        raise PermissionError("Fonte bloqueia acesso automático (403).")

    response.raise_for_status()
    return response.text


def clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator="\n")
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


# =========================
# FALLBACK ANALYZER (NO LLM)
# =========================

def fallback_read_mod(raw_text: str, url: str) -> dict:
    """
    Analyzer mínimo para garantir que o app funcione
    mesmo sem LLM.
    """
    return {
        "mod_name": "Unknown mod",
        "creator": None,
        "functional_summary": raw_text[:800],
        "confidence": "low",
        "notes": [
            "LLM indisponível ou desativado.",
            "Resumo gerado apenas por extração de texto.",
            f"URL: {url}"
        ]
    }


# =========================
# PHASE 1 ORCHESTRATOR
# =========================

def phase1_analyze_url(url: str) -> dict:
    source = detect_source(url)

    html = fetch_page(url)
    raw_text = clean_text(html)

    # 🔹 Aqui o LLM entra APENAS se existir no futuro
    lm_data = fallback_read_mod(raw_text, url)

    result = {
        "source": source,
        "url": url,
        "mod_name": lm_data.get("mod_name"),
        "creator": lm_data.get("creator"),
        "functional_summary": lm_data.get("functional_summary"),
        "confidence": lm_data.get("confidence"),
        "notes": lm_data.get("notes", []),
        "raw_text_preview": raw_text[:1000]
    }

    assert_phase1_output(result)
    return result


def assert_phase1_output(data: dict):
    required_keys = {
        "source",
        "url",
        "mod_name",
        "creator",
        "functional_summary",
        "confidence",
        "notes",
        "raw_text_preview"
    }

    assert set(data.keys()) == required_keys
    assert data["confidence"] in {"high", "medium", "low"}
    assert isinstance(data["notes"], list)


# =========================
# STREAMLIT UI
# =========================

st.title("TS4 Mod Analyzer — Phase 1")

st.markdown(
    """
Cole uma **URL de mod** (Patreon, Tumblr, Itch.io ou site do criador).

🔹 Nesta fase, o app:
- acessa a página
- extrai o texto
- gera um resumo funcional mínimo
- **não classifica**
- **não depende de LLM**
"""
)

url_input = st.text_input("URL do mod")

if st.button("Analisar"):
    if not url_input.strip():
        st.warning("Cole uma URL válida.")
    else:
        try:
            result = phase1_analyze_url(url_input)

            st.success("Análise concluída (modo seguro)")
            st.json(result)

        except PermissionError:
            st.warning(
                "A fonte bloqueia leitura automática (403).\n\n"
                "Isso é comum no CurseForge.\n"
                "Tente Patreon, Tumblr, Itch.io ou site do criador."
            )

        except Exception as e:
            st.error(f"Erro inesperado: {e}")
