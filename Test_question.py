import streamlit as st
import re
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuration des informations de l'API Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open('Nom de votre feuille de calcul').sheet1  # Remplacez 'Nom de votre feuille de calcul' par le nom de votre feuille

st.header(":mailbox: Donnez votre avis sur le livrable!")

# Form for feedback
st.subheader("Vos coordonnées:")
name = st.text_input("Nom")
surname = st.text_input("Prénom")
email = st.text_input("Adresse email")

# Vérification de l'adresse e-mail
def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)

# Add a scale for clarity of the deliverable
st.subheader("Quelle était la clarté du livrable?")
clarity_rating = st.slider(label="",
                            min_value=1,
                            max_value=10,
                            step=1,
                            value=5)

# Create a layout with "Pas clair du tout" aligned left under 1 and "Extrêmement clair" aligned right under 10
left_text = "<div style='text-align: left;'>Pas clair du tout</div>"
right_text = "<div style='text-align: right;'>Extrêmement clair</div>"

col1, col2, col3 = st.columns([1, 8, 1])
with col1:
    st.markdown(left_text, unsafe_allow_html=True)
with col2:
    st.write("")
with col3:
    st.markdown(right_text, unsafe_allow_html=True)

st.write("")
st.write("")

Commentaires = st.text_input("Commentaires")
st.write("")
st.write("")

if st.button("Envoyer"):
    if name.strip() and surname.strip() and email.strip() and validate_email(email):
        # Process the feedback
        feedback = {
            "Nom": name.strip(),
            "Prénom": surname.strip(),
            "Email": email.strip(),
            "Clarté": clarity_rating,
            "Commentaires" : Commentaires
        }
        # Placeholder for further processing (e.g., saving to database, sending email)
        st.success("Feedback envoyé avec succès !")
        
        # Ajouter une nouvelle ligne avec les données du feedback dans la feuille de calcul Google Sheets
        feedback_row = [feedback["Nom"], feedback["Prénom"], feedback["Email"], feedback["Clarté"], feedback["Commentaires"]]
        sheet.append_row(feedback_row)
    else:
        st.error("Veuillez remplir tous les champs avec des valeurs valides.")
