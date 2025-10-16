# 📦 Benötigte Libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

#SMTP konfigurieren: Für die E-Mail-Funktion musst du einen SMTP-Server eintragen (z. B. Gmail, Mailtrap, etc.)

#Datenschutz: Die App speichert keine Daten dauerhaft – du kannst sie lokal oder privat hosten.

# 🧒 Geburtsdatum deiner Tochter
geburtsdatum = datetime(2025, 10, 5)

# 📅 Impfplan mit empfohlenem Alter in Tagen
impfungen = [
    {"Name": "6-fach (1. Dosis)", "Alter_in_Tagen": 60},
    {"Name": "Pneumokokken (1. Dosis)", "Alter_in_Tagen": 60},
    {"Name": "Rotavirus (1. Dosis)", "Alter_in_Tagen": 60},
    {"Name": "6-fach (2. Dosis)", "Alter_in_Tagen": 90},
    {"Name": "Pneumokokken (2. Dosis)", "Alter_in_Tagen": 90},
    {"Name": "Rotavirus (2. Dosis)", "Alter_in_Tagen": 120},
    {"Name": "6-fach (3. Dosis)", "Alter_in_Tagen": 150},
    {"Name": "Pneumokokken (3. Dosis)", "Alter_in_Tagen": 150},
    {"Name": "MMRV (1. Dosis)", "Alter_in_Tagen": 365},
    {"Name": "6-fach (Auffrischung)", "Alter_in_Tagen": 365},
    {"Name": "Pneumokokken (Auffrischung)", "Alter_in_Tagen": 365}
]

# 🧾 DataFrame erstellen
df = pd.DataFrame(impfungen)
df["Fälligkeitsdatum"] = df["Alter_in_Tagen"].apply(lambda x: geburtsdatum + timedelta(days=x))
df["Tatsächliches Datum"] = pd.NaT
df["Status"] = "Ausstehend"

# 🖥️ Streamlit UI
st.title("🍼 Impfplan-Tracker für dein Baby")
st.write(f"Geburtsdatum: {geburtsdatum.strftime('%d.%m.%Y')}")

# 📥 Eingabe für tatsächliche Impftermine
for i, row in df.iterrows():
    impfung = row["Name"]
    faellig = row["Fälligkeitsdatum"].strftime('%d.%m.%Y')
    st.subheader(f"{impfung} (Fällig am {faellig})")
    datum = st.date_input(f"Tatsächliches Impfdatum für {impfung}", key=f"date_{i}")
    status = st.selectbox(f"Status für {impfung}", ["Ausstehend", "Geplant", "Erledigt"], key=f"status_{i}")
    df.at[i, "Tatsächliches Datum"] = datum
    df.at[i, "Status"] = status

# 📊 Gantt-Chart
st.subheader("📈 Impf-Timeline")
fig, ax = plt.subplots(figsize=(10, 6))
for i, row in df.iterrows():
    start = row["Fälligkeitsdatum"]
    end = row["Tatsächliches Datum"] if pd.notnull(row["Tatsächliches Datum"]) else start + timedelta(days=1)
    ax.barh(row["Name"], (end - start).days, left=start, color="green" if row["Status"] == "Erledigt" else "orange")
ax.set_xlabel("Datum")
ax.set_ylabel("Impfung")
plt.tight_layout()
st.pyplot(fig)

# 📤 Export als CSV
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Impfplan als CSV herunterladen", data=csv, file_name="impfplan.csv", mime="text/csv")

# 📧 E-Mail-Erinnerung (optional)
st.subheader("📧 E-Mail-Erinnerung einrichten")
email = st.text_input("Deine E-Mail-Adresse")
nachricht = st.text_area("Nachricht (z. B. nächste Impfung)")
if st.button("Erinnerung senden"):
    try:
        msg = MIMEText(nachricht)
        msg["Subject"] = "Impf-Erinnerung"
        msg["From"] = "dein@email.de"
        msg["To"] = email

        # Lokaler SMTP-Server (z. B. Gmail oder Mailtrap konfigurieren)
        with smtplib.SMTP("smtp.example.com", 587) as server:
            server.starttls()
            server.login("dein@email.de", "DEIN_PASSWORT")
            server.send_message(msg)
        st.success("E-Mail wurde gesendet!")
    except Exception as e:
        st.error(f"Fehler beim Senden: {e}")
