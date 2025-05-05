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

def generate_charts(data, t):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 " + t["performance"])
        df_bar = pd.DataFrame({
            "category": [t["reach"], t["engagement"], t["conversions"]],
            "value": [data["reach"], data["engagement"], data["conversions"]]
        })
        fig_bar = px.bar(df_bar, x="category", y="value", color="category",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        st.subheader("📈 " + t["metrics_title"])
        df_pie = pd.DataFrame({
            "category": [t["budget"], t["duration"]],
            "value": [data["budget"], data["duration"]]
        })
        fig_pie = px.pie(df_pie, values="value", names="category",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

def save_pdf(objectif, budget, duration, reach, engagement, conversions, t):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "📊 Rapport de Campagne Marketing")
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Date : {time.strftime('%d/%m/%Y')}")
    c.line(100, 725, 500, 725)
    
    # Campaign Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 700, "🔍 Détails de la Campagne")
    c.setFont("Helvetica", 12)
    c.drawString(100, 680, f"🎯 {t['objective']} : {objectif}")
    c.drawString(100, 660, f"💰 {t['budget']} : {budget} €")
    c.drawString(100, 640, f"⏱️ {t['duration']} : {duration} jours")
    
    # Metrics
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 610, "📈 Métriques de Performance")
    c.setFont("Helvetica", 12)
    c.drawString(100, 590, f"👥 {t['reach']} : {reach}")
    c.drawString(100, 570, f"💬 {t['engagement']} : {engagement}")
    c.drawString(100, 550, f"🔄 {t['conversions']} : {conversions}")
    
    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(100, 100, "Généré avec MarketPlus - Solution d'analyse marketing intelligente")
    
    c.showPage()
    c.save()
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

    # Génération PDF (disponible partout)
    st.sidebar.markdown("---")
    if st.sidebar.button(t["generate_pdf"]):
        with st.spinner("Génération du rapport..."):
            pdf_data = save_pdf(
                st.session_state.campaign_data["objectif"],
                st.session_state.campaign_data["budget"],
                st.session_state.campaign_data["duration"],
                st.session_state.campaign_data["reach"],
                st.session_state.campaign_data["engagement"],
                st.session_state.campaign_data["conversions"],
                t
            )
            
            st.sidebar.download_button(
                label=t["download_pdf"],
                data=pdf_data,
                file_name="rapport_campagne.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()