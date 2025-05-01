import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
import plotly.express as px
import pandas as pd
from io import BytesIO

# Fonction pour générer des données simulées
def generate_demo_data():
    return {
        "objectif": "Augmenter les ventes",
        "budget": random.randint(500, 5000),
        "duration": random.randint(1, 30),
        "reach": random.randint(10000, 100000),
        "engagement": random.randint(500, 10000),
        "conversions": random.randint(100, 1000)
    }

# Fonction pour générer un graphique à barres (démonstration)
def generate_bar_chart(data):
    fig = px.bar(
        data_frame=data,
        x="category",
        y="value",
        title="Analyse de la campagne"
    )
    return fig

# Fonction pour sauvegarder le PDF avec les données simulées
def save_pdf(objectif, budget, duration, reach, engagement, conversions):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Définir la police et la taille
    c.setFont("Helvetica", 12)
    
    # Titre avec un emoji (UTF-8)
    c.drawString(100, 750, "🎯 Rapport de Campagne")
    c.drawString(100, 730, f"Objectif : {objectif}")
    c.drawString(100, 710, f"Budget : {budget} €")
    c.drawString(100, 690, f"Durée : {duration} jours")
    c.drawString(100, 670, f"Portée estimée : {reach}")
    c.drawString(100, 650, f"Engagement estimé : {engagement}")
    c.drawString(100, 630, f"Conversions estimées : {conversions}")

    # Enregistrer le PDF dans un buffer
    c.showPage()
    c.save()
    
    # Retourner le contenu du PDF sous forme de bytes
    buffer.seek(0)
    return buffer.read()

# Fonction principale
def main():
    st.set_page_config(page_title="MarketPlus - Démo", layout="wide")

    # Menu latéral
    st.sidebar.title("Menu de la campagne")
    menu = st.sidebar.radio("Choisir une option", ("Tableau de bord", "Analyse", "Graphiques", "Paramètres"))

    # Générer des données simulées
    data = generate_demo_data()

    # Utiliser session_state pour garder les valeurs des paramètres
    if 'objectif' not in st.session_state:
        st.session_state.objectif = data['objectif']
        st.session_state.budget = data['budget']
        st.session_state.duration = data['duration']
        st.session_state.reach = data['reach']
        st.session_state.engagement = data['engagement']
        st.session_state.conversions = data['conversions']

    # Page Tableau de bord
    if menu == "Tableau de bord":
        st.title("Tableau de bord de la campagne")
        st.write(f"**Objectif** : {st.session_state.objectif}")
        st.write(f"**Budget** : {st.session_state.budget} €")
        st.write(f"**Durée** : {st.session_state.duration} jours")
        st.write(f"**Portée estimée** : {st.session_state.reach}")
        st.write(f"**Engagement estimé** : {st.session_state.engagement}")
        st.write(f"**Conversions estimées** : {st.session_state.conversions}")

        st.markdown("---")
        st.write("🔔 **Données réelles disponibles dans la version Premium.**")
        st.button("Passer à la version Premium")

    # Page Analyse
    elif menu == "Analyse":
        st.title("Analyse détaillée de la campagne")
        st.write(f"Objectif de la campagne : {st.session_state.objectif}")
        st.write(f"Budget total : {st.session_state.budget} €")
        st.write(f"Durée estimée : {st.session_state.duration} jours")
        
        st.markdown("### Détails de l'engagement")
        st.write(f"Portée estimée : {st.session_state.reach}")
        st.write(f"Engagement estimé : {st.session_state.engagement}")
        st.write(f"Conversions estimées : {st.session_state.conversions}")
        
        st.markdown("---")
        st.write("🔔 **Version Premium pour des données réelles et plus d'analyses.**")
        st.button("Passer à la version Premium")

    # Page Graphiques
    elif menu == "Graphiques":
        st.title("Graphiques de la campagne")
        graph_data = {
            "category": ["Budget", "Portée estimée", "Engagement estimé", "Conversions estimées"],
            "value": [st.session_state.budget, st.session_state.reach, st.session_state.engagement, st.session_state.conversions]
        }
        df = pd.DataFrame(graph_data)
        fig = generate_bar_chart(df)
        st.plotly_chart(fig)

        st.markdown("---")
        st.write("🔔 **Accédez à plus de graphiques et visualisations avec la version Premium.**")
        st.button("Passer à la version Premium")

    # Page Paramètres
    elif menu == "Paramètres":
        st.title("Paramètres de la campagne")
        st.write("Vous pouvez ajuster les paramètres ci-dessous pour simuler différentes configurations de campagne.")
        
        objectif = st.text_input("Objectif de la campagne", value=st.session_state.objectif)
        budget = st.number_input("Budget en €", min_value=1, max_value=10000, value=st.session_state.budget)
        duration = st.number_input("Durée en jours", min_value=1, max_value=365, value=st.session_state.duration)
        reach = st.number_input("Portée estimée", min_value=1000, max_value=1000000, value=st.session_state.reach)
        engagement = st.number_input("Engagement estimé", min_value=1, max_value=100000, value=st.session_state.engagement)
        conversions = st.number_input("Conversions estimées", min_value=1, max_value=10000, value=st.session_state.conversions)

        if st.button("Mettre à jour les données de la campagne"):
            # Mettre à jour les valeurs dans session_state
            st.session_state.objectif = objectif
            st.session_state.budget = budget
            st.session_state.duration = duration
            st.session_state.reach = reach
            st.session_state.engagement = engagement
            st.session_state.conversions = conversions

            st.write("Les données de la campagne ont été mises à jour.")
            st.write(f"Nouvelle portée estimée : {reach}")
            st.write(f"Nouvelle engagement estimée : {engagement}")
            st.write(f"Nouvelle conversions estimées : {conversions}")

        st.markdown("---")
        st.write("🔔 **Passez à la version Premium pour personnaliser davantage.**")
        st.button("Passer à la version Premium")

    # Générer le PDF
    if st.button("Générer le rapport PDF"):
        # Passer les valeurs mises à jour
        pdf_bytes = save_pdf(st.session_state.objectif, st.session_state.budget, st.session_state.duration, 
                             st.session_state.reach, st.session_state.engagement, st.session_state.conversions)
        st.download_button(
            label="📄 Télécharger le rapport PDF",
            data=pdf_bytes,
            file_name="rapport_campagne.pdf",
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()
