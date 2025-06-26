import streamlit as st
import psycopg2

# 🔌 Verbindung zur Supabase-Datenbank über secrets.toml
try:
    conn = psycopg2.connect(
        host=st.secrets["db_host"],
        user=st.secrets["db_user"],
        password=st.secrets["db_password"],
        dbname=st.secrets["db_name"],
        port=st.secrets["db_port"]
    )
    cursor = conn.cursor()
except Exception as e:
    st.error(f"❌ Fehler beim Aufbau der Datenbankverbindung: {e}")
    st.stop()

st.title("🔍 Artikeldetails anzeigen")

# 🧾 Eingabefeld für Artikelnummer
artikelnummer = st.text_input("Artikelnummer eingeben:")

# 🔍 Datenbankabfrage
if artikelnummer:
    try:
        cursor.execute("""
            SELECT
                Rabattgruppe,
                Rabattgruppename,
                ArtikelPreiseinheit,
                LagerME,
                Mengeneinheit,
                Spartenbez,
                ArtikelBez,
                ArtikelgruppeBez,
                HauptgruppeBez,
                WarengruppeBez
            FROM artikel
            WHERE Artikel = %s
            LIMIT 1
        """, (artikelnummer,))
        result = cursor.fetchone()
    except Exception as e:
        st.error(f"❌ Fehler bei der Datenabfrage: {e}")
        result = None

    if result:
        (
            rabattgruppe, rabattgruppename, einheit,
            lagerme, menge, spartenbez, artikelbez,
            artikelgruppe, hauptgruppe, warengruppe
        ) = result

        st.success(f"✅ Artikel gefunden: {artikelbez}")
        st.markdown(f"**Artikelnummer:** `{artikelnummer}`")
        st.markdown(f"**Rabattgruppe:** {rabattgruppe}")
        st.markdown(f"**Rabattgruppename:** {rabattgruppename}")
        st.markdown(f"**Preiseinheit:** {einheit}")
        st.markdown(f"**Lagereinheit:** {lagerme}")
        st.markdown(f"**Mengeneinheit:** {menge}")
        st.markdown(f"**Spartenbezeichnung:** {spartenbez}")
        st.markdown(f"**Artikelgruppe:** {artikelgruppe}")
        st.markdown(f"**Hauptgruppe:** {hauptgruppe}")
        st.markdown(f"**Warengruppe:** {warengruppe}")
    else:
        st.error("❌ Kein Artikel mit dieser Nummer gefunden.")

# 🔒 Verbindung schließen
cursor.close()
conn.close()
