# streamlit run C:\Users\qliksense\Deckungsbeitragsrechnung\Test.py


import streamlit as st
import psycopg2

# Verbindung zur PostgreSQL-Datenbank
def get_connection():
    return psycopg2.connect(
        dbname="Deckungsbeitragsrechnung",
        user="postgres",
        password="Mayer#79513",
        host="localhost",
        port="5432"
    )

# Spaltennamen definieren
SPALTEN = [
    "Artikel", "Rabattgruppe", "Rabattgruppename", "ArtikelPreiseinheit",
    "LagerME", "Mengeneinheit", "Spartenbez", "ArtikelBez",
    "ArtikelgruppeBez", "HauptgruppeBez", "WarengruppeBez"
]

# UI
st.title("🔍 Artikeldaten anzeigen")

artikelnummer = st.text_input("Artikelnummer eingeben:")

# Nur abfragen, wenn was eingegeben wurde
if artikelnummer.strip():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM artikel WHERE Artikel = %s
        """, (artikelnummer,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            st.success("✅ Artikel gefunden")
            daten = dict(zip(SPALTEN, result))
            st.write("### 📄 Details:")
            for key, value in daten.items():
                st.markdown(f"- **{key}**: {value}")
        else:
            st.warning("❗ Artikelnummer nicht gefunden.")

    except Exception as e:
        st.error(f"Fehler beim Zugriff auf die Datenbank: {e}")
