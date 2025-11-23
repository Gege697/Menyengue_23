import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# Fichier de stockage
# -----------------------------
DATA_FILE = "geotech_data.xlsx"

if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=[
        "NomChantier", "Date", "TypeSol", "Granulometrie", "TeneurEau", "Commentaires"
    ])
    df_init.to_excel(DATA_FILE, index=False)

# -----------------------------
# Page principale
# -----------------------------
st.title("📋 Collecte de données géotechniques d'un sol")
st.write("Remplissez le formulaire pour enregistrer vos observations sur le sol.")

# Formulaire de collecte
with st.form("form_geotech"):
    nom_chantier = st.text_input("Nom du chantier")
    date_prelev = st.date_input("Date du prélèvement")
    type_sol = st.selectbox("Type de sol", ["Sable", "Gravier", "Argile", "Limon", "Autre"])
    granulometrie = st.selectbox("Granulométrie dominante", ["0-2 mm", "2-5 mm", "5-20 mm", ">20 mm"])
    teneur_eau = st.number_input("Teneur en eau (%)", min_value=0.0, max_value=100.0, step=0.1)
    commentaires = st.text_area("Commentaires (optionnel)")
    submit = st.form_submit_button("Enregistrer")

# Enregistrement des données
if submit:
    if not nom_chantier:
        st.error("Le nom du chantier est obligatoire.")
    else:
        try:
            df = pd.read_excel(DATA_FILE)
        except:
            df = pd.DataFrame(columns=[
                "NomChantier", "Date", "TypeSol", "Granulometrie", "TeneurEau", "Commentaires"
            ])
        new_row = pd.DataFrame({
            "NomChantier": [nom_chantier],
            "Date": [date_prelev],
            "TypeSol": [type_sol],
            "Granulometrie": [granulometrie],
            "TeneurEau": [teneur_eau],
            "Commentaires": [commentaires]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(DATA_FILE, index=False)
        st.success("✅ Données enregistrées !")

# -----------------------------
# Visualisation des données
# -----------------------------
st.subheader("📊 Aperçu des résultats")

def plot_pie(variable, title):
    try:
        df_plot = pd.read_excel(DATA_FILE)
        if variable not in df_plot.columns or df_plot[variable].empty:
            st.info(f"Aucune donnée pour {variable}.")
            return
        counts = df_plot[variable].value_counts()
        fig, ax = plt.subplots()
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
        ax.axis('equal')
        ax.set_title(title)
        st.pyplot(fig)
    except:
        st.info("Pas encore de données.")

# Diagrammes circulaires pour variables qualitatives
plot_pie("TypeSol", "Distribution des types de sol")
plot_pie("Granulometrie", "Distribution des granulométries")

# Histogramme pour la variable quantitative
try:
    df_plot = pd.read_excel(DATA_FILE)
    if not df_plot.empty:
        fig, ax = plt.subplots()
        ax.hist(df_plot["TeneurEau"].dropna(), bins=10, color="#FFA07A")
        ax.set_xlabel("Teneur en eau (%)")
        ax.set_ylabel("Nombre d'observations")
        ax.set_title("Distribution de la teneur en eau")
        st.pyplot(fig)
except:
    st.info("Pas encore de données quantitatives.")
