#%%
import ollama
import time
import sys
from ollama._types import Options
import nltk
from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
import re
from sklearn.feature_extraction.text import TfidfVectorizer


# Fonction pour vérifier si une ressource nltk est disponible
def download_nltk_resource(resource):
    try:
        nltk.data.find(resource)
    except LookupError:
        nltk.download(resource.split("/")[-1])


# Fonction pour filtrer les mots
def clean_keywords(lemmatizer_name, keyword_list):
    cleaned = set()

    # Liste des mots en anglais
    english_words = set(words.words())

    for phrase in keyword_list:
        # Découper en mots et lemmatiser
        words_in_phrase = phrase.lower().split()
        lemmatized_words = [lemmatizer_name.lemmatize(word) for word in words_in_phrase]
        lemmatized_phrase = " ".join(lemmatized_words)

        # Vérifier si chaque mot est un mot valide OU si l'expression entière fait sens
        if all(word in english_words for word in lemmatized_words) or lemmatized_phrase in english_words:
            # Vérifier qu'il ne s'agit pas d'une chaîne sans sens
            if not re.match(r"^[a-z]\d+$", lemmatized_phrase):
                cleaned.add(lemmatized_phrase)
    return list(cleaned)


#%%
# Appeler le modèle avec stream=True
def analyse_LLM(article_text):

    # Vérifier et télécharger les ressources si nécessaire
    download_nltk_resource('corpora/wordnet')
    download_nltk_resource('corpora/omw-1.4')
    download_nltk_resource('corpora/words')



    prompt ="""
    You are a highly skilled scientific assistant. Please analyze the following article thoroughly and provide a detailed yet structured summary. Focus exclusively on the core scientific content, excluding non-essential details such as acknowledgments, funding sources, references, author information, and redundant introductory sections. The summary should comprehensively explain:

    1. The scientific context and the main research objectives, including the motivation behind the study.
    2. The methodology and approaches used, with enough detail to understand the experimental or theoretical framework.
    3. The key results and findings, including numerical data and trends where relevant.
    4. The conclusions and implications, discussing their significance, limitations, and possible future directions.

    Maintain high scientific accuracy, preserving as much relevant detail as possible while keeping the summary clear and well-structured.

    Article:
    
    """


    # Combiner le prompt avec l'article
    full_input = prompt + "\n" + article_text

    time_start = time.time()


    options_values = Options(

        # load time options
        numa        = None,
        num_ctx     = None,
        num_batch   = None,
        num_gpu     = None,
        main_gpu    = None,
        low_vram    = None,
        f16_kv      = None,
        logits_all  = None,
        vocab_only  = None,
        use_mmap    = None,
        use_mlock   = None,
        embedding_only = None,
        num_thread  = None,

        # runtime options
        num_keep    = None,
        seed        = None,
        num_predict = None,
        top_k       = None,
        top_p       = None,
        tfs_z       = None,
        typical_p   = None,
        repeat_last_n = None,
        temperature = 0.0,
        repeat_penalty = None,
        presence_penalty = None,
        frequency_penalty = None,
        mirostat        = None,
        mirostat_tau = None,
        mirostat_eta = None,
        penalize_newline = None,
        stop = None,
        )

    response_iterator = ollama.generate(
        model='mistral',  # Le modèle que tu utilises
        prompt= full_input,  # Tes messages à envoyer au modèle
        stream=True,  # Activer le streaming
        options = options_values
    )

    # Variable pour stocker la réponse partielle
    partial_response = ""
    print("Waiting for the LLM to write a summary:\n")
    # Traiter la réponse au fur et à mesure de son arrivée
    for response in response_iterator:
        # Récupérer le contenu du message généré jusqu'à présent
        new_content = response['response']
        
        # Ajouter le nouveau contenu à la réponse partielle
        partial_response += new_content
        
        # Afficher l'accumulation de texte sans retour à la ligne
        sys.stdout.write(new_content)
        sys.stdout.flush()  # Forcer l'affichage immédiat du texte
        
        #time.sleep(0.1)  # Optionnel : ralentir légèrement l'affichage pour plus de fluidité

    time_stop = time.time()
    print(f"\nTime needed : {time_stop - time_start:.2f}\n")



    # Texte à traiter
    text = [article_text]

    # Initialisation du modèle TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_features=100, ngram_range=(1, 8))
    X = vectorizer.fit_transform(text)

    # Extraction des mots-clés
    keywords = vectorizer.get_feature_names_out()

    # Affichage des mots-clés
    print(f"Keywords detected with Tfid algorithm: \n\n{keywords}\n")

    # Initialisation du lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Appliquer le nettoyage
    filtered_keywords = (clean_keywords(lemmatizer, keywords))

    # Filtrer pour ne garder que les formes singulières
    unique_keywords = list(set(lemmatizer.lemmatize(word) for word in filtered_keywords))

    # Convertir en une chaîne séparée par des virgules
    keywords_str = ", ".join(sorted(unique_keywords))
    print(f"Keyword cleaned with lemmatizer algorithm: \n\n{keywords_str} \n\n")

    # %%
    prompt = """Contexte :
    J’ai extrait une liste de mots clés à partir d’articles scientifiques, mais elle contient des termes inutiles comme des numéros de section, des mots trop génériques et des doublons au pluriel.

    Tâche :
    Nettoie cette liste en appliquant les règles suivantes :

    Supprime les numéros, symboles et codes non pertinents (ex : i10, 2b, fig1).
    Garde les termes scientifiques et élimine les mots trop courants qui n’apportent pas de valeur.
    Ne garde que la version au singulier si un mot apparaît aussi sous sa forme plurielle.
    Conserve les expressions multi-mots si elles sont plus informatives qu’un mot seul.
    Retourne la liste triée par ordre alphabétique, sous forme de texte avec les mots séparés par des virgules.
    Exemple d’entrée :
    ["neuron", "neurons", "activation", "synapse", "fig1", "experiment", "experiments", "i10", "learning rate"]

    Exemple de sortie attendue :
    "activation, experiment, learning rate, neuron, synapse"

    Format de sortie attendue : 

    Seule une liste en sortie est attendue, c'est primordial que cette liste retournée soit séparée par des virgules, sans commentaire ni explication.

    Voici la liste à nettoyer :
    """

    full_input = prompt + "\n" + keywords_str



    options_values = Options(
        temperature = 0.0,)


    response_iterator = ollama.generate(
        model='mistral',  # Le modèle que tu utilises
        prompt= full_input,  # Tes messages à envoyer au modèle
        stream=True,  # Activer le streaming
        options = options_values,
    )

    # Variable pour stocker la réponse partielle
    partial_response = ""
    print("Keywords cleaned with LLM\n")
    time_start = time.time()
    # Traiter la réponse au fur et à mesure de son arrivée
    for response in response_iterator:
        # Récupérer le contenu du message généré jusqu'à présent
        new_content = response['response']
        
        # Ajouter le nouveau contenu à la réponse partielle
        partial_response += new_content
        
        # Afficher l'accumulation de texte sans retour à la ligne
        sys.stdout.write(new_content)
        sys.stdout.flush()  # Forcer l'affichage immédiat du texte
        
        #time.sleep(0.1)  # Optionnel : ralentir légèrement l'affichage pour plus de fluidité

    time_stop = time.time()
    print(f"\nTime needed : {time_stop - time_start:.2f}\n\n\n")


    #%%


    prompt = """Context:
    I am providing you with a list of keywords extracted from a scientific article. Your task is to:

    Extract the main topics: Groups of associated keywords that represent general research areas in the article.
    Expand the keywords: Add related terms, synonyms, or expressions that can strengthen the categorization of the article in a database.
    Instructions:

    The main topics should be more general, with each topic potentially including several keywords.
    The expanded keywords should be related to the specific domain and can include additional terms that help link the article to other articles.
    Avoid including overly vague or general terms, but rather focus on more detailed concepts.
    Organize the output into two sections: one for the topics and one for the expanded keywords.
    Expected output format:

    Main Topics: 
    - Topic 1: {general topic 1, detailed topic, etc.}
    - Topic 2: {general topic 2, detailed topic, etc.}

    Expanded Keywords: 
    - keyword 1, expanded keyword 1, expanded keyword 2
    - keyword 2, expanded keyword 1, expanded keyword 2

    List of extracted keywords from the article:

    """

    full_input = prompt + "\n" + partial_response



    options_values = Options(
        temperature = 0.0,)


    response_iterator = ollama.generate(
        model='mistral',  # Le modèle que tu utilises
        prompt= full_input,  # Tes messages à envoyer au modèle
        stream=True,  # Activer le streaming
        options = options_values,
    )

    # Variable pour stocker la réponse partielle
    partial_response = ""
    print("Topics and expanded keywords by LLM\n")


    time_start = time.time()
    # Traiter la réponse au fur et à mesure de son arrivée
    for response in response_iterator:
        # Récupérer le contenu du message généré jusqu'à présent
        new_content = response['response']
        
        # Ajouter le nouveau contenu à la réponse partielle
        partial_response += new_content
        
        # Afficher l'accumulation de texte sans retour à la ligne
        sys.stdout.write(new_content)
        sys.stdout.flush()  # Forcer l'affichage immédiat du texte
        
        #time.sleep(0.1)  # Optionnel : ralentir légèrement l'affichage pour plus de fluidité

    time_stop = time.time()
    print(f"\nTime needed : {time_stop - time_start:.2f}\n\n\n")

