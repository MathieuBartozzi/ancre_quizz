# import streamlit as st
# import plotly.graph_objects as go
# import pandas as pd
# from io import BytesIO
# import seaborn as sns
# import matplotlib.pyplot as plt


# # Charger les propositions depuis le fichier 'propositions.txt'
# def load_propositions(file_path="propositions.txt"):
#     with open(file_path, "r", encoding="utf-8") as file:
#         propositions = [line.strip() for line in file if line.strip()]
#     return propositions

# # Initialiser les propositions et vérifier les états
# propositions = load_propositions()
# if 'current_proposition' not in st.session_state:
#     st.session_state.current_proposition = 0
# if 'responses' not in st.session_state:
#     st.session_state.responses = [None] * len(propositions)
# if 'show_results_button' not in st.session_state:
#     st.session_state.show_results_button = False
# if 'show_results' not in st.session_state:
#     st.session_state.show_results = False
# if 'top_propositions_selected' not in st.session_state:
#     st.session_state.top_propositions_selected = False
# if 'selected_top_propositions' not in st.session_state:
#     st.session_state.selected_top_propositions = []
# if 'test_started' not in st.session_state:
#     st.session_state.test_started = False

# # Définir les ancres de carrière et les indices des propositions associées
# career_anchors = {
#     "TECH": [1, 10, 19, 28, 37],
#     "MG": [2, 11, 20, 29, 38],
#     "AUT": [3, 12, 21, 30, 39],
#     "SEC": [4, 13, 22, 31, 40],
#     "CRE": [5, 14, 23, 32, 41],
#     "CAU": [6, 15, 24, 33, 42],
#     "DEF": [7, 16, 25, 34, 43],
#     "VIE": [8, 17, 26, 35, 44],
#     "INTER": [9, 18, 27, 36, 45],
# }

# # Calculer les scores pour chaque ancre en tenant compte des réponses
# def calculate_scores(selected_propositions=None):
#     scores = {anchor: 0 for anchor in career_anchors.keys()}
#     for anchor, indices in career_anchors.items():
#         scores[anchor] = sum(st.session_state.responses[i-1] for i in indices if st.session_state.responses[i-1] is not None)

#     # Ajouter les 4 points pour les propositions sélectionnées par l'utilisateur
#     if selected_propositions:
#         for p in selected_propositions:
#             for anchor, indices in career_anchors.items():
#                 if p in indices:
#                     scores[anchor] += 4

#     return scores

# # Calculer les scores et les trier du meilleur au plus faible
# scores = calculate_scores(selected_propositions=st.session_state.selected_top_propositions)
# sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=False)
# labels, values = zip(*sorted_scores)  # Séparer les étiquettes et les valeurs pour l'affichage


# # Afficher l'introduction et le bouton "Commencer le test"
# if not st.session_state.test_started:
#     st.title("Test des Ancres de Carrière")
#     st.write("""
#         Les **ancres de carrière** sont des éléments fondamentaux qui influencent vos choix professionnels en fonction de vos valeurs, compétences et motivations profondes.
#         Ce test vous aide à identifier ce qui vous motive réellement dans votre carrière.

#         Le test comprend **45 propositions**, et il vous faudra environ **15 minutes** pour le compléter. Pour chaque proposition, vous évaluerez votre degré d'accord sur une échelle de 1 à 5 :

#         - **1** : Tout à fait en désaccord
#         - **2** : Plutôt en désaccord
#         - **3** : Sans opinion
#         - **4** : Plutôt d'accord
#         - **5** : Tout à fait d'accord

#         Prenez le temps de répondre honnêtement pour obtenir des résultats qui reflètent fidèlement vos préférences professionnelles.
#     """)
#     if st.button("Commencer le test"):
#         st.session_state.test_started = True
#         st.rerun()

# # Afficher les résultats une fois le questionnaire terminé et après la sélection
# elif st.session_state.show_results and st.session_state.top_propositions_selected:

#     st.title("Vos résultats 👀")
#     # Calcul des scores pour les ancres de carrière avec les propositions sélectionnées
#     scores = calculate_scores(st.session_state.selected_top_propositions)
#     scores_df = pd.DataFrame(sorted_scores, columns=["Ancre", "Score"])

#     # Créer un graphique en barres horizontal
#     plt.figure(figsize=(10, 6))
#     sns.barplot(x="Score", y="Ancre", data=scores_df, palette="crest")

#     #enleve le cadre
#     sns.despine()

#     # Ajouter un titre et afficher le graphique
#     plt.xlabel("Score")
#     st.pyplot(plt)  # Afficher le graphique dans Streamlit



# # Conteneur avec bordures pour le bloc des ancres de carrière
#     with st.container(border=True):

#         # Explication globale
#         st.subheader("Comprendre vos ancres de carrière")
#         st.write("""
#         Les ancres de carrière reflètent les motivations et les valeurs profondes qui guident vos choix professionnels.
#         Elles vous aident à identifier ce qui est le plus important pour vous dans votre parcours professionnel.
#         """)

#         # Structure des lignes pour afficher les ancres avec des préfixes en gras
#         rows = [
#             ["TECH", "MG", "AUT"],
#             ["SEC", "CRE", "DEF"],
#             ["CAU", "VIE", "INTER"]
#         ]

#         # Descriptions des ancres
#         descriptions = {
#             "TECH": "L’ancre technique : La carrière s’organise autour d’un métier spécifique. Le salarié souhaite devenir un expert dans son domaine et acquérir sans cesse de nouvelles compétences pour se perfectionner.",
#             "MG": "L’ancre managériale : La carrière est dirigée vers les postes de direction. Le salarié entend changer de poste régulièrement et franchir les étapes les unes après les autres pour se rapprocher du sommet de la hiérarchie.",
#             "AUT": "L’ancre autonomie : La carrière s’appuie sur un besoin d’indépendance et d’autonomie. Le salarié cherche avant tout à être libre dans ses décisions professionnelles, et peut quitter l’entreprise pour se concentrer sur des projets personnels.",
#             "SEC": "L’ancre sécurité-stabilité : La carrière est orientée vers une zone de confort. Le salarié est peu susceptible d’accepter un changement de poste ou une mobilité géographique.",
#             "CRE": "L’ancre créativité : La carrière est fondée avant tout sur le besoin de créer. Le salarié préfère se tourner vers des entreprises innovantes et est susceptible de lancer sa propre activité.",
#             "CAU": "L’ancre devouement : La carrière s’oriente sur une activité perçue comme une cause, par exemple travailler pour une entreprise alignée avec ses centres d’intérêt.",
#             "DEF": "L’ancre défi : La carrière est définie par la nécessité de se confronter à des obstacles pour les dépasser, comme partir à l’étranger ou changer de secteur.",
#             "VIE": "L’ancre style de vie : La carrière est centrée sur la recherche de la qualité de vie. L'équilibre entre vie privée et professionnelle est primordial.",
#             "INTER": "La carrière est tournée vers la mobilité à l’international, plaçant l’étranger et la découverte de nouvelles cultures au cœur du projet professionnel."
#         }

#         # Création de l'affichage en 3 lignes avec 3 colonnes
#         for row in rows:
#             col1, col2, col3 = st.columns(3)

#             with col1:
#                 ancre = row[0]
#                 with st.popover(ancre):
#                     st.write(f"{descriptions[ancre]}")  # Affiche le préfixe en gras et la description

#             with col2:
#                 ancre = row[1]
#                 with st.popover(ancre):
#                     st.write(f"{descriptions[ancre]}")  # Affiche le préfixe en gras et la description

#             with col3:
#                 ancre = row[2]
#                 with st.popover(ancre):
#                     st.write(f"{descriptions[ancre]}")  # Affiche le préfixe en gras et la description

#     # Aligner les boutons sur toute la largeur

#     col1, col2, col3 = st.columns(3)

#     with col1:
#     # Créer un buffer pour sauvegarder l'image Seaborn
#         img_buffer = BytesIO()

#         # Sauvegarder l'image Seaborn dans le buffer en format PNG
#         plt.savefig(img_buffer, format="png", bbox_inches="tight")
#         img_buffer.seek(0)  # Replacer le curseur au début du buffer pour le téléchargement

#         # Bouton de téléchargement de l'image
#         st.download_button(
#             label="Télécharger l'image",
#             data=img_buffer,
#             file_name="resultats_ancres_de_carriere_seaborn.png",
#             mime="image/png"
#         )


#     with col2:
#         # Option de téléchargement du fichier CSV des scores
#         scores_df = pd.DataFrame(sorted_scores, columns=["Ancre", "Score"])  # Créer le DataFrame à partir des scores triés
#         csv = scores_df.to_csv(index=False).encode('utf-8')
#         st.download_button(
#             label="Télécharger les scores",
#             data=csv,
#             file_name="resultats_ancres_de_carriere.csv",
#             mime="text/csv"
#         )

#     with col3:
#         # Bouton pour recommencer le test
#         if st.button("Recommencer le test"):
#             st.session_state.current_proposition = 0
#             st.session_state.responses = [None] * len(propositions)
#             st.session_state.show_results_button = False
#             st.session_state.show_results = False
#             st.session_state.top_propositions_selected = False
#             st.session_state.selected_top_propositions = []
#             st.session_state.test_started = False
#             st.rerun()

# # Sélection des 3 propositions parmi les 10 avec les plus hauts scores
# elif st.session_state.show_results_button and not st.session_state.top_propositions_selected:
#     st.title("Mes meilleures propositions ✨")
#     # Récupérer les 10 propositions avec les scores les plus élevés
#     response_scores = [(i+1, score) for i, score in enumerate(st.session_state.responses) if score is not None]
#     top_propositions = sorted(response_scores, key=lambda x: x[1], reverse=True)[:10]

#     st.write("Sélectionnez 3 propositions parmi celles qui ont les scores les plus élevés et avec lesquelles vous êtes le plus en accord :")

#     # Afficher les 10 propositions les plus élevées avec des cases à cocher
#     selected = []
#     for i, (prop_index, score) in enumerate(top_propositions):
#         if st.checkbox(f"Proposition {prop_index}: {propositions[prop_index - 1]} (Score: {score})", key=f"top_{i}"):
#             selected.append(prop_index)

#     # Valider la sélection des 3 propositions
#     if len(selected) == 3:
#         if st.button("Valider la sélection"):
#             st.session_state.selected_top_propositions = selected
#             st.session_state.top_propositions_selected = True
#             st.rerun()
#     elif len(selected) > 3:
#         st.warning("Veuillez sélectionner uniquement 3 propositions.")

# # Afficher la page des propositions si le test est en cours
# elif not st.session_state.show_results_button:
#     # Afficher la barre de progression
#     progress = st.progress(st.session_state.current_proposition / len(propositions))

#     # Créer le formulaire pour la proposition actuelle
#     st.title("Test en cours 📝")
#     with st.form("proposition_form"):
#         proposition = propositions[st.session_state.current_proposition]
#         st.write(f"Proposition {st.session_state.current_proposition + 1} : {proposition}")

#         # Générer une clé unique pour chaque question
#         response_key = f"response_{st.session_state.current_proposition}"

#         # Afficher les options de réponse avec une clé unique
#         response = st.radio(
#             "Choisissez une réponse",
#             [1, 2, 3, 4, 5],
#             index=st.session_state.responses[st.session_state.current_proposition] - 1 if st.session_state.responses[st.session_state.current_proposition] is not None else 0,
#             key=response_key  # Utiliser une clé unique
#         )

#         # Boutons de navigation
#         col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
#         with col1:
#             previous = st.form_submit_button("Préc.")
#         with col2:
#             next = st.form_submit_button("Suiv.")

#         # Enregistrer immédiatement la réponse
#         st.session_state.responses[st.session_state.current_proposition] = response

#     # Gérer la navigation
#     if previous and st.session_state.current_proposition > 0:
#         st.session_state.current_proposition -= 1
#         st.rerun()
#     elif next:
#         if st.session_state.current_proposition < len(propositions) - 1:
#             st.session_state.current_proposition += 1
#             st.rerun()
#         else:
#             st.session_state.show_results_button = True
#             st.rerun()

# # Afficher le bouton "Afficher les résultats" une fois le questionnaire terminé
# elif st.session_state.show_results_button:
#     st.write("Vous avez terminé le test. Cliquez sur le bouton ci-dessous pour afficher vos résultats.")

#     # Afficher les ballons
#     st.balloons()

#     if st.button("Afficher les résultats"):
#         st.session_state.show_results = True
#         st.rerun()


import streamlit as st
import pandas as pd
from io import BytesIO
import seaborn as sns
import matplotlib.pyplot as plt

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
    "TECH": [1, 10, 19, 28, 37],
    "MG": [2, 11, 20, 29, 38],
    "AUT": [3, 12, 21, 30, 39],
    "SEC": [4, 13, 22, 31, 40],
    "CRE": [5, 14, 23, 32, 41],
    "CAU": [6, 15, 24, 33, 42],
    "DEF": [7, 16, 25, 34, 43],
    "VIE": [8, 17, 26, 35, 44],
    "INTER": [9, 18, 27, 36, 45],
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

# Afficher les résultats sous forme de graphique classé
def display_sorted_results(scores):
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    scores_df = pd.DataFrame(sorted_scores, columns=["Ancre", "Score"])
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Score", y="Ancre", data=scores_df, palette="crest")
    sns.despine()
    plt.xlabel("Score")
    st.pyplot(plt)
    return scores_df

# Afficher l'introduction et le bouton pour commencer le test
def display_intro():
    st.title("Test des Ancres de Carrière")
    st.write("""
        Les **ancres de carrière** influencent vos choix professionnels selon vos valeurs, compétences et motivations profondes.
        Ce test vous aidera à identifier ce qui vous motive réellement dans votre carrière.

        Le test comprend **45 propositions**, avec une échelle de 1 à 4 pour chaque :
        - **1** : Pas du tout d’accord
        - **2** : Plutôt pas d’accord
        - **3** : Plutôt d’accord
        - **4** : Tout à fait d’accord
    """)

    st.write("Vous souhaitez découvrir ce qui vous motive vraiment ? Installez vous confortablement ☕️ et cliquez ci-dessous pour débuter le test.")

    if st.button("Commencer le test"):
        st.session_state.test_started = True
        st.rerun()

# Afficher le questionnaire avec navigation
def display_questionnaire(propositions):
    progress = st.progress(st.session_state.current_proposition / len(propositions))
    proposition = propositions[st.session_state.current_proposition]
    st.title("Test en cours 📝")
    with st.form("proposition_form"):
        st.write(f"Proposition {st.session_state.current_proposition + 1} : {proposition}")
        response = st.radio(
            "Choisissez une réponse",
            [1, 2, 3, 4],
            format_func=lambda x: ["Pas du tout d’accord", "Plutôt pas d’accord", "Plutôt d’accord", "Tout à fait d’accord"][x-1],
            index=(st.session_state.responses[st.session_state.current_proposition] - 1) if st.session_state.responses[st.session_state.current_proposition] else 0
        )
        col1, col2 = st.columns([1, 7])
        with col1:
            previous = st.form_submit_button("Préc.")
        with col2:
            next = st.form_submit_button("Suiv.",type="primary")
        st.session_state.responses[st.session_state.current_proposition] = response
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
    with st.expander("Comprendre vos ancres de carrière"):
        # st.subheader("Comprendre vos ancres de carrière")
        st.write("""
            Les ancres de carrière reflètent les motivations et les valeurs profondes qui guident vos choix professionnels.
            Elles vous aident à identifier ce qui est le plus important pour vous dans votre parcours professionnel.
        """)

        # Structure et descriptions des ancres
        rows = [
            ["TECH", "MG", "AUT"],
            ["SEC", "CRE", "DEF"],
            ["CAU", "VIE", "INTER"]
        ]
        descriptions = {
            "TECH": "L’ancre technique. Votre carrière s’organise autour d’un métier spécifique. Vous souhaitez devenir un expert dans votre domaine et acquérir sans cesse de nouvelles compétences pour vous perfectionner.",
            "MG": "L’ancre managériale. Votre carrière est orientée vers les postes de direction. Vous envisagez de changer de poste régulièrement pour franchir les étapes et vous rapprocher du sommet de la hiérarchie.",
            "AUT": "L’ancre autonomie. Votre carrière repose sur un besoin d’indépendance et d’autonomie. Vous cherchez avant tout à être libre dans vos décisions professionnelles et pourriez même quitter votre entreprise pour vous concentrer sur des projets personnels.",
            "SEC": "L’ancre sécurité-stabilité. Votre carrière est orientée vers une zone de confort. Vous êtes peu susceptible d’accepter un changement de poste ou une mobilité géographique.",
            "CRE": "L’ancre créativité. Votre carrière est fondée avant tout sur le besoin de créer. Vous préférez vous tourner vers des entreprises innovantes et pourriez envisager de lancer votre propre activité.",
            "CAU": "L’ancre dévouement. Votre carrière s’oriente vers une activité perçue comme une cause, par exemple travailler pour une entreprise alignée avec vos centres d’intérêt.",
            "DEF": "L’ancre défi. Votre carrière est définie par la nécessité de vous confronter à des obstacles pour les dépasser, comme partir à l’étranger ou changer de secteur.",
            "VIE": "L’ancre style de vie. Votre carrière est centrée sur la recherche de la qualité de vie. L’équilibre entre vie privée et vie professionnelle est primordial pour vous.",
            "INTER": "L’ancre internationale. Votre carrière est tournée vers la mobilité à l’international, plaçant l’étranger et la découverte de nouvelles cultures au cœur de votre projet professionnel."
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
            data=img_buffer,
            file_name="resultats_ancres_de_carriere_seaborn.png",
            mime="image/png"
        )
    with col2:
        csv = scores_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Télécharger les scores",
            data=csv,
            file_name="resultats_ancres_de_carriere.csv",
            mime="text/csv"
        )
    with col3:
        if st.button("Recommencer le test"):
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
