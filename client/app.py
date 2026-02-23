from __future__ import annotations

import sqlite3

import streamlit as st

try:
    from client.paths import db_path
except ModuleNotFoundError:  # fallback when script path is client/
    from paths import db_path


def init_db() -> str:
    database = db_path()
    with sqlite3.connect(database) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS app_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            "INSERT INTO app_events(description) VALUES (?)",
            ("Aplicação iniciada",),
        )
        conn.commit()
    return str(database)


def main() -> None:
    st.set_page_config(page_title="FarmSaaS Rural", page_icon="🌾", layout="wide")
    st.title("FarmSaaS Rural")
    st.caption("Aplicativo desktop executando com Streamlit")

    database_location = init_db()
    st.success("Banco local pronto para uso.")
    st.code(database_location, language="text")


if __name__ == "__main__":
    main()
