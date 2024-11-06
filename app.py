import streamlit as st
import pandas as pd
from io import BytesIO
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


# Charger les propositions depuis le fichier 'propositions.txt'
def load_propositions(file_path="propositions.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]

# Initialiser les états de session pour le test
def initialize_session_states(propositions):
    if 'current_proposition' not in st.session_state:
        st.session_state.current_proposition = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = [None] * len(propositions)
    if 'show_results_button' not in st.session_state:
        st.session_state.show_results_button = False
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'top_propositions_selected' not in st.session_state:
        st.session_state.top_propositions_selected = False
    if 'selected_top_propositions' not in st.session_state:
        st.session_state.selected_top_propositions = []
    if 'test_started' not in st.session_state:
        st.session_state.test_started = False

# Configurer les ancres de carrière et les indices associés
career_anchors = {
    "technique": [1, 10, 19, 28, 37],
    "managériale": [2, 11, 20, 29, 38],
    "autonomie": [3, 12, 21, 30, 39],
    "sécurité-stabilité": [4, 13, 22, 31, 40],
    "créativité": [5, 14, 23, 32, 41],
    "dévouement": [6, 15, 24, 33, 42],
    "défi": [7, 16, 25, 34, 43],
    "style de vie": [8, 17, 26, 35, 44],
    "internationale": [9, 18, 27, 36, 45],
}


# Calculer les scores pour chaque ancre
def calculate_scores(selected_propositions=None):
    scores = {anchor: 0 for anchor in career_anchors.keys()}
    for anchor, indices in career_anchors.items():
        scores[anchor] = sum(
            st.session_state.responses[i - 1] for i in indices if st.session_state.responses[i - 1] is not None
        )
    if selected_propositions:
        for p in selected_propositions:
            for anchor, indices in career_anchors.items():
                if p in indices:
                    scores[anchor] += 4
    return scores

# # Afficher les résultats sous forme de graphique classé
# def display_sorted_results(scores):
#     sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#     scores_df = pd.DataFrame(sorted_scores, columns=["Ancre", "Score"])
#     plt.figure(figsize=(10, 6))
#     sns.barplot(x="Score", y="Ancre", data=scores_df, palette="crest")
#     sns.despine()
#     plt.xlabel("Score")
#     st.pyplot(plt)
#     return scores_df


# Afficher les résultats sous forme de graphique classé avec Plotly
import plotly.express as px

# Afficher les résultats sous forme de graphique classé avec Plotly et palette de test de personnalité
def display_sorted_results(scores):
    # Trier les scores
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    scores_df = pd.DataFrame(sorted_scores, columns=["Ancre", "Score"])

    # Créer le graphique barplot avec Plotly et appliquer un dégradé de couleur basé sur le score
    fig = px.bar(
        scores_df,
        x="Score",
        y="Ancre",
        orientation='h',
        color="Score",  # Utiliser la colonne Score pour générer le dégradé
        color_continuous_scale="Blugrn",  # Utiliser un dégradé de couleurs
    )

    # Personnaliser le style du graphique pour masquer les éléments non désirés
    fig.update_layout(
        showlegend=False,               # Masquer la légende
        xaxis_title=None,               # Masquer le titre de l'axe des scores
        yaxis_title=None,               # Masquer le titre de l'axe des ancres
        coloraxis_showscale=False,
        yaxis=dict(categoryorder="total ascending"),  # Trier les ancres par score
        template="plotly_white"
    )

    # Afficher le graphique dans Streamlit
    st.plotly_chart(fig)

    return scores_df



# Afficher l'introduction et le bouton pour commencer le test
def display_intro():
    st.title("Test des Ancres de Carrière")

    # Diviser en deux colonnes
    col1, col2 = st.columns([2, 1])  # Largeur de colonnes (texte: 2/3, image: 1/3)

    # Afficher le texte dans la première colonne
    with col1:
        st.write("""
            Les **ancres de carrière** influencent vos choix professionnels en fonction de vos valeurs, vos compétences et vos aspirations. Ce test vous aidera à identfier ce qui vous motive vraiment dans votre carrière.
            Il comprend 45 propositions à évaluer sur une échelle de 1 à 5 :
            - **1** : Pas du tout d’accord
            - **2** : Plutôt pas d’accord
            - **3** : Ni d’accord ni pas d’accord
            - **4** : Plutôt d’accord
            - **5** : Tout à fait d’accord

            Il n’y a pas de bonnes ou de mauvaises réponses. L’important est de répondre avec honnêteté et de manière intuitive 😊.

        """)

    # Afficher l'image dans la deuxième colonne
    with col2:
        st.image("image.jpg", use_column_width=True)  # Ajuste l'image à la largeur de la colonne

    st.write("""
        Installez-vous confortablement ☕️ et cliquez ci-dessous pour débuter le test.""")

    if st.button("Commencer le test", type="primary"):
        st.session_state.test_started = True
        st.rerun()

    st.divider()
    st.write("*Adapté de Schein, E. H. (1990). Career Anchors: Discovering Your Real Values. Pfeiffer & Company, San Diego, California, et mis à jour avec l'ancre internationale par Jean-Luc Cerdin.*")

def display_questionnaire(propositions):
    # Afficher la progression du test
    progress = st.progress((st.session_state.current_proposition + 1) / len(propositions))

    # Récupérer la question actuelle
    proposition = propositions[st.session_state.current_proposition]
    st.title("Test en cours 📝")

    # Formulaire pour chaque question
    with st.form("proposition_form"):
        st.write(f"Proposition {st.session_state.current_proposition + 1} : {proposition}")

        # Initialiser la réponse si elle n'existe pas
        if f"response_{st.session_state.current_proposition}" not in st.session_state:
            st.session_state[f"response_{st.session_state.current_proposition}"] = None

        # Gérer l'index du bouton radio
        if st.session_state[f"response_{st.session_state.current_proposition}"] is None:
            response_index = 0  # Valeur par défaut sans sélection
        else:
            response_index = st.session_state[f"response_{st.session_state.current_proposition}"] - 1

        # Créer le bouton radio avec l'index approprié
        response = st.radio(
            "Choisissez une réponse",
            [1, 2, 3, 4,5],
            index=response_index,
            format_func=lambda x: ["1: Pas du tout d’accord", "2: Plutôt pas d’accord", "3: Ni d’accord ni pas d’accord","4: Plutôt d’accord", "5: Tout à fait d’accord"][x - 1],
            key=f"radio_{st.session_state.current_proposition}"  # Clé unique pour chaque question
        )

        # Boutons de navigation
        col1, col2 = st.columns([1, 7])
        with col1:
            previous = st.form_submit_button("Préc.")
        with col2:
            next = st.form_submit_button("Suiv.", type="primary")

        # Enregistrer la réponse pour la question actuelle
        if response in [1, 2, 3, 4, 5]:
            st.session_state[f"response_{st.session_state.current_proposition}"] = response

    # Mettre à jour la liste des réponses pour l'analyse des résultats
    st.session_state.responses[st.session_state.current_proposition] = st.session_state[f"response_{st.session_state.current_proposition}"]

    # Gérer la navigation entre les questions
    if previous and st.session_state.current_proposition > 0:
        st.session_state.current_proposition -= 1
        st.rerun()
    elif next:
        if st.session_state.current_proposition < len(propositions) - 1:
            st.session_state.current_proposition += 1
            st.rerun()
        else:
            st.session_state.show_results_button = True
            st.rerun()


# Afficher la sélection des propositions les plus élevées
def display_top_propositions_selection():
    st.title("Mes meilleures propositions ✨")
    response_scores = [(i + 1, score) for i, score in enumerate(st.session_state.responses) if score is not None]
    top_propositions = sorted(response_scores, key=lambda x: x[1], reverse=True)[:10]

    st.write("Sélectionnez 3 propositions parmi celles qui ont les scores les plus élevés et avec lesquelles vous êtes le plus en accord :")
    with st.container(border=True):
        selected = []
        for i, (prop_index, score) in enumerate(top_propositions):
            if st.checkbox(f"Proposition {prop_index}: {propositions[prop_index - 1]} (Score: {score})", key=f"top_{i}"):
                selected.append(prop_index)

        if len(selected) == 3:
            if st.button("Valider la sélection"):
                st.session_state.selected_top_propositions = selected
                st.session_state.top_propositions_selected = True
                st.rerun()
        elif len(selected) > 3:
            st.warning("Veuillez sélectionner uniquement 3 propositions.")

# Afficher la page des résultats avec les descriptions et options de téléchargement
def display_results():
    st.title("Vos résultats 👀")
    scores = calculate_scores(st.session_state.selected_top_propositions)
    scores_df = display_sorted_results(scores)

    # Conteneur avec bordures pour le bloc des ancres de carrière
    with st.container(border=True):
        st.subheader("Comprendre vos ancres de carrière")
        # st.subheader("Comprendre vos ancres de carrière")
        st.write("""
            Les ancres de carrière reflètent les motivations et les valeurs profondes qui guident vos choix professionnels.
            Elles vous aident à identifier ce qui est le plus important pour vous dans votre parcours professionnel.
        """)

        # Structure et descriptions des ancres
        rows = [
            ["technique", "managériale", "autonomie"],
            ["sécurité", "créativité", "défi"],
            ["dévouement", "style de vie", "internationale"]
        ]
        descriptions = {
            "technique": "**L’ancre technique**. Votre carrière s’organise autour d’un métier spécifique. Vous souhaitez devenir un expert dans votre domaine et acquérir sans cesse de nouvelles compétences pour vous perfectionner.",
            "managériale": "**L’ancre managériale**. Votre carrière est orientée vers les postes de direction. Vous envisagez de changer de poste régulièrement pour franchir les étapes et vous rapprocher du sommet de la hiérarchie.",
            "autonomie": "**L’ancre autonomie**. Votre carrière repose sur un besoin d’indépendance et d’autonomie. Vous cherchez avant tout à être libre dans vos décisions professionnelles et pourriez même quitter votre entreprise pour vous concentrer sur des projets personnels.",
            "sécurité": "**L’ancre sécurité-stabilité**. Votre carrière est orientée vers une zone de confort. Vous êtes peu susceptible d’accepter un changement de poste ou une mobilité géographique.",
            "créativité": "**L’ancre créativité**. Votre carrière est fondée avant tout sur le besoin de créer. Vous préférez vous tourner vers des entreprises innovantes et pourriez envisager de lancer votre propre activité.",
            "dévouement": "**L’ancre dévouement**. Votre carrière s’oriente vers une activité perçue comme une cause, par exemple travailler pour une entreprise alignée avec vos centres d’intérêt.",
            "défi": "**L’ancre défi**. Votre carrière est définie par la nécessité de vous confronter à des obstacles pour les dépasser, comme partir à l’étranger ou changer de secteur.",
            "style de vie": "**L’ancre style de vie**. Votre carrière est centrée sur la recherche de la qualité de vie. L’équilibre entre vie privée et vie professionnelle est primordial pour vous.",
            "internationale": "**L’ancre internationale**. Votre carrière est tournée vers la mobilité à l’international, plaçant l’étranger et la découverte de nouvelles cultures au cœur de votre projet professionnel."
            }

        for row in rows:
            col1, col2, col3 = st.columns(3)

            with col1:
                ancre = row[0]
                with st.popover(ancre):
                    st.write(f"{descriptions[ancre]}")  # Affiche le préfixe en gras et la description

            with col2:
                ancre = row[1]
                with st.popover(ancre):
                    st.write(f"{descriptions[ancre]}")  # Affiche le préfixe en gras et la description

            with col3:
                ancre = row[2]
                with st.popover(ancre):
                    st.write(f"{descriptions[ancre]}")  # Affiche le préfixe en gras et la description


    # Options de téléchargement des résultats
    col1, col2, col3 = st.columns(3)
    with col1:
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format="png", bbox_inches="tight")
        img_buffer.seek(0)
        st.download_button(
            label="Télécharger l'image",
            type="primary",
            data=img_buffer,
            file_name="resultats_ancres_de_carriere_seaborn.png",
            mime="image/png"
        )
    with col2:
        csv = scores_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les scores",
            type="primary",
            data=csv,
            file_name="resultats_ancres_de_carriere.csv",
            mime="text/csv"
        )
    with col3:
        if st.button("Recommencer le test",type="primary"):
            st.session_state.current_proposition = 0
            st.session_state.responses = [None] * len(propositions)
            st.session_state.show_results_button = False
            st.session_state.show_results = False
            st.session_state.top_propositions_selected = False
            st.session_state.selected_top_propositions = []
            st.session_state.test_started = False
            st.rerun()

# Exécution principale de l'application
def main():
    global propositions
    propositions = load_propositions()
    initialize_session_states(propositions)

    if not st.session_state.test_started:
        display_intro()
    elif st.session_state.show_results:
        display_results()
    elif st.session_state.show_results_button and not st.session_state.top_propositions_selected:
        display_top_propositions_selection()
    elif st.session_state.show_results_button and not st.session_state.show_results:
        st.title("Test terminé ✅")
        st.write("Félicitations, vous avez terminé le test 🥳! Cliquez sur le bouton ci-dessous pour afficher vos résultats.")
        if st.button("Afficher les résultats"):
            st.session_state.show_results = True
            st.rerun()
    else:
        display_questionnaire(propositions)

if __name__ == "__main__":
    main()
