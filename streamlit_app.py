import streamlit as st
import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup


# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="TS4 Mod Analyzer — Phase 1",
    layout="centered"
)

REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


# =========================
# FETCH
# =========================

def fetch_page(url: str) -> str:
    response = requests.get(
        url,
        headers=REQUEST_HEADERS,
        timeout=20
    )

    if response.status_code == 403:
        # 403 é esperado (CurseForge / Patreon)
        return response.text

    response.raise_for_status()
    return response.text


# =========================
# IDENTITY EXTRACTION
# =========================

def extract_identity(html: str, url: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    page_title = soup.title.string.strip() if soup.title else None

    og_title = None
    og_site = None

    for meta in soup.find_all("meta"):
        if meta.get("property") == "og:title":
            og_title = meta.get("content")
        if meta.get("property") == "og:site_name":
            og_site = meta.get("content")

    slug = (
        urlparse(url).path
        .replace("-", " ")
        .replace("/", " ")
        .strip()
        or None
    )

    return {
        "page_title": page_title,
        "og_title": og_title,
        "og_site": og_site,
        "url_slug": slug
    }


# =========================
# NORMALIZATION
# =========================

def normalize_identity(identity: dict) -> dict:
    mod_name = (
        identity.get("og_title")
        or identity.get("page_title")
        or identity.get("url_slug")
    )

    creator = identity.get("og_site")

    if creator and " on " in creator:
        creator = creator.replace(" on Patreon", "").strip()

    if mod_name and " - " in mod_name:
        mod_name = mod_name.split(" - ")[0].strip()

    if mod_name and "|" in mod_name:
        mod_name = mod_name.split("|")[0].strip()

    return {
        "mod_name": mod_name,
        "creator": creator,
    }


# =========================
# ORCHESTRATOR
# =========================

def analyze_url(url: str) -> dict:
    html = fetch_page(url)

    identity_raw = extract_identity(html, url)
    identity_norm = normalize_identity(identity_raw)

    return {
        "url": url,
        "mod_name": identity_norm.get("mod_name"),
        "creator": identity_norm.get("creator"),
        "identity_debug": identity_raw,
    }


# =========================
# UI
# =========================

st.title("TS4 Mod Analyzer — Phase 1")

st.markdown(
    """
Cole a **URL de um mod** (CurseForge, Patreon, site pessoal).

O app **não lê conteúdo fechado**.
Ele extrai apenas **identidade confiável** para evitar duplicatas.
"""
)

url_input = st.text_input(
    "URL do mod",
    placeholder="https://www.curseforge.com/sims4/mods/..."
)

if st.button("Analisar"):
    if not url_input.strip():
        st.warning("Cole uma URL válida.")
    else:
        try:
            result = analyze_url(url_input)

            st.success("Identidade extraída com sucesso")

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("📦 Mod")
                st.write(result["mod_name"] or "—")

            with col2:
                st.subheader("👤 Criador")
                st.write(result["creator"] or "—")

            with st.expander("🔍 Detalhes técnicos (debug)"):
                st.json(result["identity_debug"])

        except Exception as e:
            st.error(f"Erro inesperado: {e}")
