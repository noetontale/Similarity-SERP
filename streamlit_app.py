import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()
api_key = os.getenv("VALUE_SERP_API_KEY")

# Fonction pour nettoyer les URLs en enlevant les paramètres après 'srsltid'
def clean_url(url):
    return url.split('?srsltid=')[0]

# Fonction pour récupérer les URLs des résultats Value SERP pour un mot-clé donné
def get_value_serp_urls(query):
    params = {
        'api_key': api_key,
        'q': query,
        'gl': 'fr',
        'google_domain': 'google.fr'
    }
    
    # Effectuer la requête HTTP GET à VALUE SERP
    api_result = requests.get('https://api.valueserp.com/search', params=params)
    
    # Vérifier que la requête a réussi
    if api_result.status_code == 200:
        results = api_result.json().get('organic_results', [])[:10]  # Limiter à 10 résultats
        # Nettoyer les URLs en supprimant les paramètres après 'srsltid'
        return [clean_url(result['link']) for result in results if 'link' in result]
    else:
        st.error(f"Erreur lors de la récupération des résultats : {api_result.status_code}")
        return []

# Fonction pour comparer les URLs de deux mots-clés sans tenir compte de la position
def compare_keyword_urls(query1, query2):
    urls1 = set(get_value_serp_urls(query1))
    urls2 = set(get_value_serp_urls(query2))
    
    # Calculer le nombre d'URLs similaires
    similar_urls_count = len(urls1.intersection(urls2))
    
    # Calculer le pourcentage de similarité basé sur un total fixe de 10
    similarity_percentage = round((similar_urls_count / 10) * 100, 1)
    
    return similarity_percentage, similar_urls_count, urls1, urls2

# Interface Streamlit
st.title("Comparaison des URLs dans les SERP pour les mots-clés")
st.write("Cet outil compare les URLs des résultats Google pour deux mots-clés donnés en français.")

# Entrée utilisateur
keyword1 = st.text_input("Entrez le premier mot-clé")
keyword2 = st.text_input("Entrez le deuxième mot-clé")

# Comparer les URLs
if st.button("Comparer"):
    if api_key and keyword1 and keyword2:
        st.write("Récupération des URLs et calcul de similarité...")
        similarity_percentage, similar_urls_count, urls1, urls2 = compare_keyword_urls(keyword1, keyword2)
        
        st.write(f"Similarité entre les URLs : {similarity_percentage}%")
        st.write(f"Nombre d'URLs similaires : {similar_urls_count} / 10")
        st.write(f"URLs pour '{keyword1}':")
        st.write(list(urls1))
        st.write(f"URLs pour '{keyword2}':")
        st.write(list(urls2))
    else:
        st.error("Veuillez vérifier votre clé API et les mots-clés.")
