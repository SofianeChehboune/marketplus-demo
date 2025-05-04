import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import random
import plotly.express as px
import pandas as pd
from io import BytesIO
from PIL import Image
import base64
import os
import time

# ---------- MULTILINGUE ----------
translations = {
    "fr": {
        "app_title": "🎯 MarketPlus - Version Démo",
        "welcome_banner": "📢 Découvrez comment booster vos campagnes avec l'intelligence des données !",
        "welcome_sub": "Optimisez vos performances marketing en quelques clics avec <b>MarketPlus</b> 💡",
        "premium_title": "🔐 Accès Premium",
        "enter_code": "Entrez votre code Premium",
        "code_valid": "✅ Mode Premium activé - Fonctionnalités débloquées !",
        "code_invalid": "❌ Code incorrect - Essayez 'PREMIUM2025'",
        "dashboard": "📊 Tableau de bord de la campagne",
        "analysis": "📈 Analyse détaillée",
        "charts": "📊 Graphiques de la campagne",
        "settings": "⚙️ Paramètres de la campagne",
        "menu": "Menu",
        "objective": "Objectif",
        "budget": "Budget (€)",
        "duration": "Durée (jours)",
        "reach": "Portée",
        "engagement": "Engagement",
        "conversions": "Conversions",
        "update_success": "✅ Paramètres mis à jour avec succès !",
        "generate_pdf": "📄 Générer le rapport PDF",
        "download_pdf": "📥 Télécharger le PDF",
        "premium_info": "🔒 Version limitée - Activez le mode Premium pour débloquer toutes les fonctionnalités",
        "language": "🌐 Langue",
        "contact": "🔗 Me contacter sur LinkedIn",
        "signature": "🏅 Réalisé par Sofiane Chehboune<br>✅ 9 ans en gestion, ≈ 3 ans en Data Analysis et ML<br>📊 Python, Streamlit, PyGWalker, Plotly,...",
        "metrics_title": "📈 Métriques Clés",
        "performance": "🚀 Performance de la Campagne",
        "recommendations": "💡 Recommandations Intelligentes",
        "premium_button": "🚀 Accéder à la Version Premium",
        "premium_page": "💎 Version Premium",
        "premium_features": "🚀 Boostez votre expérience utilisateur",
        "premium_description": "La version <strong>Premium</strong> vous donne accès à des fonctionnalités avancées, un support prioritaire et bien plus encore !",
        "watch_video": "🎥 Voir la vidéo explicative",
        "upgrade": "🛒 Passer à la version Premium",
        "contact_us": "📩 Une question ? Contactez-nous",
        "your_name": "Votre nom",
        "your_email": "Votre e-mail",
        "your_message": "Votre message",
        "send": "Envoyer",
        "thanks": "✅ Merci ! Nous vous répondrons rapidement."
    },
    "en": {
        "app_title": "🎯 MarketPlus - Demo Version",
        "welcome_banner": "📢 Discover how to boost your campaigns with data intelligence!",
        "welcome_sub": "Optimize your marketing performance in a few clicks with <b>MarketPlus</b> 💡",
        "premium_title": "🔐 Premium Access",
        "enter_code": "Enter your Premium code",
        "code_valid": "✅ Premium mode activated - Features unlocked!",
        "code_invalid": "❌ Incorrect code - Try 'PREMIUM2025'",
        "dashboard": "📊 Campaign Dashboard",
        "analysis": "📈 Detailed Analysis",
        "charts": "📊 Campaign Charts",
        "settings": "⚙️ Campaign Settings",
        "menu": "Menu",
        "objective": "Objective",
        "budget": "Budget (€)",
        "duration": "Duration (days)",
        "reach": "Reach",
        "engagement": "Engagement",
        "conversions": "Conversions",
        "update_success": "✅ Settings updated successfully!",
        "generate_pdf": "📄 Generate PDF Report",
        "download_pdf": "📥 Download PDF",
        "premium_info": "🔒 Limited version - Activate Premium mode to unlock all features",
        "language": "🌐 Language",
        "contact": "🔗 Contact me on LinkedIn",
        "signature": "🏅 Created by Sofiane Chehboune<br>✅ 9 years in management, ≈ 3 years in Data Analysis and ML<br>📊 Python, Streamlit, PyGWalker, Plotly,...",
        "metrics_title": "📈 Key Metrics",
        "performance": "🚀 Campaign Performance",
        "recommendations": "💡 Smart Recommendations",
        "premium_button": "🚀 Access Premium Version",
        "premium_page": "💎 Premium Version",
        "premium_features": "🚀 Boost your user experience",
        "premium_description": "The <strong>Premium</strong> version gives you access to advanced features, priority support and much more!",
        "watch_video": "🎥 Watch explanatory video",
        "upgrade": "🛒 Upgrade to Premium",
        "contact_us": "📩 Any questions? Contact us",
        "your_name": "Your name",
        "your_email": "Your email",
        "your_message": "Your message",
        "send": "Send",
        "thanks": "✅ Thank you! We'll get back to you soon."
    },
    "ar": {
        "app_title": "🎯 ماركت بلس - النسخة التجريبية",
        "welcome_banner": "📢 اكتشف كيف تعزز حملاتك بذكاء البيانات!",
        "welcome_sub": "حسّن أداءك التسويقي بسهولة مع <b>ماركت بلس</b> 💡",
        "premium_title": "🔐 الوصول المميز",
        "enter_code": "أدخل رمز Premium",
        "code_valid": "✅ تم تفعيل الوضع المميز - الميزات متاحة الآن!",
        "code_invalid": "❌ الرمز غير صحيح - جرب 'PREMIUM2025'",
        "dashboard": "📊 لوحة تحكم الحملة",
        "analysis": "📈 التحليل التفصيلي",
        "charts": "📊 الرسوم البيانية للحملة",
        "settings": "⚙️ إعدادات الحملة",
        "menu": "القائمة",
        "objective": "الهدف",
        "budget": "الميزانية (€)",
        "duration": "المدة (أيام)",
        "reach": "الوصول",
        "engagement": "التفاعل",
        "conversions": "التحويلات",
        "update_success": "✅ تم تحديث الإعدادات بنجاح!",
        "generate_pdf": "📄 توليد تقرير PDF",
        "download_pdf": "📥 تحميل PDF",
        "premium_info": "🔒 هذه النسخة محدودة - قم بتفعيل الوضع المميز لفتح جميع الميزات",
        "language": "🌐 اللغة",
        "contact": "🔗 تواصل معي عبر لينكدإن",
        "signature": "🏅 أنجزه سفيان شهبون<br>✅ 9 سنوات في الإدارة، ≈ 3 سنوات في تحليل البيانات وتعلم الآلة<br>📊 Python، Streamlit، PyGWalker، Plotly...",
        "metrics_title": "📈 المقاييس الرئيسية",
        "performance": "🚀 أداء الحملة",
        "recommendations": "💡 توصيات ذكية",
        "premium_button": "🚀 الوصول إلى النسخة المميزة",
        "premium_page": "💎 النسخة المميزة",
        "premium_features": "🚀 عزز تجربة المستخدم الخاصة بك",
        "premium_description": "النسخة <strong>المميزة</strong> تمنحك إمكانية الوصول إلى ميزات متقدمة ودعم أولي وغير ذلك الكثير!",
        "watch_video": "🎥 مشاهدة الفيديو التوضيحي",
        "upgrade": "🛒 الترقية إلى النسخة المميزة",
        "contact_us": "📩 لديك سؤال؟ اتصل بنا",
        "your_name": "اسمك",
        "your_email": "بريدك الإلكتروني",
        "your_message": "رسالتك",
        "send": "إرسال",
        "thanks": "✅ شكرًا! سوف نرد عليك قريبًا."
    }
}

# ---------- BASE FUNCTIONS ----------
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
    return buffer

def display_metrics(data, t):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label=t["reach"], value=f"{data['reach']:,}", delta="+12% vs attente")
    
    with col2:
        st.metric(label=t["engagement"], value=f"{data['engagement']:,}", delta="+8% vs attente")
    
    with col3:
        st.metric(label=t["conversions"], value=f"{data['conversions']:,}", delta="+15% vs attente")

def display_recommendations(t):
    st.subheader(t["recommendations"])
    with st.expander("💡 Voir les recommandations"):
        st.success("✅ Augmenter le budget de 15% pour maximiser la portée")
        st.warning("⚠️ Optimiser les créneaux horaires pour améliorer l'engagement")
        st.info("ℹ️ Tester de nouvelles créations publicitaires pour booster les conversions")

def show_premium_page(t):
    st.markdown(f"## {t['premium_page']}")
    
    # Encadré de présentation
    st.markdown(f"""
    <div style='background-color:#f9f1ff; padding:15px; border-radius:10px; border:1px solid #d1b3ff'>
        <h4>{t['premium_features']}</h4>
        <p>{t['premium_description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bouton pour voir la vidéo
    if st.button(t["watch_video"]):
        st.video("https://www.youtube.com/watch?v=TON_ID_VIDEO")  # Remplace par ton lien YouTube

        
    
    # Lien vers la page d'achat
    st.markdown(f"""
    ### {t['upgrade']}
    <div style="display:flex; gap:20px; margin:20px 0;">
    <div style="flex:2; background:#f8f5ff; padding:20px; border-radius:10px;">
        <h4 style="color:#6e00ff;">Pourquoi passer à la version Premium ?</h4>
        <ul style="padding-left:20px;">
            <li>📈 <strong>Analyses avancées</strong> - Découvrez des insights exclusifs</li>
            <li>🚀 <strong>Performances accrues</strong> - Jusqu'à 3x plus efficace</li>
            <li>🛡️ <strong>Sécurité renforcée</strong> - Protection des données premium</li>
            <li>🤝 <strong>Support prioritaire</strong> - Réponse en moins de 2h</li>
        </ul>
        
    <a href="https://votre-lien-achat.com" target="_blank">
        <button style="background:linear-gradient(135deg, #6e00ff, #a100ff); color:white; 
                        border:none; padding:12px 24px; border-radius:8px; font-size:16px; 
                        cursor:pointer; margin-top:10px;">
                Débloquer toutes les fonctionnalités
            </button>
        </a>
    </div>
    
    <div style="flex:1; background:#fff; padding:20px; border-radius:10px; box-shadow:0 2px 10px rgba(0,0,0,0.1);">
        <div style="display:flex; align-items:center; margin-bottom:15px;">
            <img src="sofiane.jpg" style="width:50px; height:50px; border-radius:50%; margin-right:10px;">
            <div>
                <h5 style="margin:0;">Sofiane Ch.</h5>
                <div style="color:gold;">★★★★★</div>
            </div>
        </div>
        <p style="font-style:italic; color:#555;">
            "MarketPlus Premium a transformé notre façon de faire du marketing. Les rapports avancés nous ont permis d'augmenter notre ROI de 40% en 3 mois seulement !"
        </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    
    
    # Formulaire de contact
    st.markdown("---")
    st.markdown(f"### {t['contact_us']}")
    
    with st.form("contact_form"):
        name = st.text_input(t["your_name"])
        email = st.text_input(t["your_email"])
        message = st.text_area(t["your_message"])
        
        submitted = st.form_submit_button(t["send"])
        
        if submitted:
            st.success(t["thanks"])

# ---------- MAIN ----------
def main():
    st.set_page_config(page_title="MarketPlus", layout="wide", page_icon="📈")
    
    # CSS personnalisé
    st.markdown("""
    <style>
        .main {background-color: #f9f9f9;}
        .stButton>button {border-radius: 8px; padding: 8px 16px;}
        .stTextInput>div>div>input {border-radius: 8px;}
        .stNumberInput>div>div>input {border-radius: 8px;}
        .metric {border-left: 4px solid #4e79a7; padding-left: 15px;}
        .st-bb {background-color: white;}
        .st-at {background-color: #f0f2f6;}
        div[data-testid="stExpander"] div[role="button"] p {font-size: 16px;}
    </style>
    """, unsafe_allow_html=True)
    
    # Langue
    langue = st.sidebar.selectbox("🌐 Langue", ["Français", "English", "العربية"])
    code_langue = {"Français": "fr", "English": "en", "العربية": "ar"}[langue]
    t = translations[code_langue]

    # Header avec onglets
    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #6e8efb, #a777e3);padding:20px;border-radius:10px;color:white;margin-bottom:20px;">
        <h1 style="color:white;margin:0;">{t["app_title"]}</h1>
        <p style="margin:0;opacity:0.9;">{t["welcome_sub"]}</p>
    </div>
    """, unsafe_allow_html=True)

    # Section Premium
    st.sidebar.markdown(f"## {t['premium_title']}")
    premium_code = "PREMIUM2025"
    code_saisi = st.sidebar.text_input(t["enter_code"], type="password", help="Essayez 'PREMIUM2025' pour la démo")
    
    premium_activated = st.session_state.get("premium_activated", False)
    if code_saisi and not premium_activated:
        if code_saisi == premium_code:
            st.session_state.premium_activated = True
            st.sidebar.success(t["code_valid"])
            # Bouton d'accès à la version premium
            st.sidebar.markdown(
                f"""
                <a href="https://marketpulse-ai-cioz3bh3tuv3vf5swqgqwu.streamlit.app/" target="_blank">
                    <button style="width:100%;background-color:#4CAF50;color:white;padding:10px;border:none;border-radius:5px;margin-top:10px;margin-bottom:20px;">
                        {t['premium_button']}
                    </button>
                </a>
                """,
                unsafe_allow_html=True
            )
        else:
            st.sidebar.error(t["code_invalid"])
    
    if not premium_activated:
        st.sidebar.warning(t["premium_info"])

    # Signature et contact
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"<small>{t['signature']}</small>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <a href="https://www.linkedin.com/in/sofiane-chehboune-5b243766/" target="_blank">
        <button style="width:100%;background-color:#0a66c2;color:white;padding:10px;border:none;border-radius:5px;margin-top:20px;">
            {t['contact']}
        </button>
    </a>
    """, unsafe_allow_html=True)

    # Initialisation des données de session
    if "campaign_data" not in st.session_state:
        st.session_state.campaign_data = generate_demo_data()

    # Menu principal
    menu = st.sidebar.radio(t["menu"],
                          [t["dashboard"], t["analysis"], t["charts"], t["settings"], t["premium_page"]],
                          label_visibility="collapsed")

    # Contenu principal
    if menu == t["dashboard"]:
        st.subheader(f"📊 {t['dashboard']}")
        
        # Métriques en haut
        display_metrics(st.session_state.campaign_data, t)
        
        # Graphiques
        generate_charts(st.session_state.campaign_data, t)
        
        # Recommandations
        if premium_activated:
            display_recommendations(t)
        else:
            st.warning(t["premium_info"])

    elif menu == t["analysis"]:
        st.subheader(f"📈 {t['analysis']}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("""
            ## Analyse des Performances
            Cette section fournit une analyse approfondie de votre campagne marketing.
            """)
            
            df = pd.DataFrame({
                "Jour": range(1, st.session_state.campaign_data["duration"] + 1),
                "Engagement": [random.randint(100, 1000) for _ in range(st.session_state.campaign_data["duration"])],
                "Conversions": [random.randint(10, 100) for _ in range(st.session_state.campaign_data["duration"])]
            })
            
            fig = px.line(df, x="Jour", y=["Engagement", "Conversions"],
                         title="Évolution quotidienne des performances",
                         color_discrete_sequence=["#4e79a7", "#f28e2b"])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("""
            ## Insights Clés
            - Taux d'engagement moyen: 4.5%
            - Coût par conversion: €12.50
            - ROI estimé: 3.2x
            """)
            
            if premium_activated:
                st.success("""
                🔍 Insights Premium:
                - Meilleur créneau horaire: 14h-16h
                - Audience la plus réceptive: 25-34 ans
                """)
            else:
                st.info("Activez le mode Premium pour obtenir des insights avancés")

    elif menu == t["charts"]:
        st.subheader(f"📊 {t['charts']}")
        
        tab1, tab2, tab3 = st.tabs(["Principaux indicateurs", "Analyse temporelle", "Comparaisons"])
        
        with tab1:
            generate_charts(st.session_state.campaign_data, t)
        
        with tab2:
            st.write("Analyse temporelle à venir...")
        
        with tab3:
            st.write("Fonctionnalité Premium - Comparaison avec les campagnes précédentes")
            if not premium_activated:
                st.warning(t["premium_info"])

    elif menu == t["settings"]:
        st.subheader(f"⚙️ {t['settings']}")
        
        with st.form("campaign_settings"):
            st.session_state.campaign_data["objectif"] = st.text_input(
                f"🎯 {t['objective']}",
                st.session_state.campaign_data["objectif"]
            )
            
            cols = st.columns(2)
            with cols[0]:
                st.session_state.campaign_data["budget"] = st.number_input(
                    f"💰 {t['budget']}",
                    value=st.session_state.campaign_data["budget"],
                    min_value=0
                )
                st.session_state.campaign_data["reach"] = st.number_input(
                    f"👥 {t['reach']}",
                    value=st.session_state.campaign_data["reach"],
                    min_value=0
                )
            
            with cols[1]:
                st.session_state.campaign_data["duration"] = st.number_input(
                    f"⏱️ {t['duration']}",
                    value=st.session_state.campaign_data["duration"],
                    min_value=1
                )
                st.session_state.campaign_data["conversions"] = st.number_input(
                    f"🔄 {t['conversions']}",
                    value=st.session_state.campaign_data["conversions"],
                    min_value=0
                )
            
            if st.form_submit_button("💾 Sauvegarder les paramètres"):
                st.success(t["update_success"])
                time.sleep(1)
                st.rerun()
    
    elif menu == t["premium_page"]:
        show_premium_page(t)

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
