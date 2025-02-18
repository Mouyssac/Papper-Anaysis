import re
import requests

# Texte brut des références
references = """1 B. Abeles, P. Sheng, M. Coutts and Y. Arie, Adv. Phys., 1975,24, 407–461.
2 J. E. Morris and T. J. Coutts, Thin Solid Films, 1977, 47, 3–65.
3 I. S. Beloborodov, A. V. Lopatin, V. M. Vinokur andK. B. Efetov, Rev. Mod. Phys., 2007, 79, 469–518.
4 M. Zhao, B. Gao, J. Tang, H. Qian and H. Wu, Appl. Phys.Rev., 2020, 7, 011301."""

# Regex pour extraire chaque référence
pattern = r"\d+\s+([^,]+),\s+([^,]+),\s+(\d{4}),\s*(\d+),\s*([\d–\-]+)"
matches = re.findall(pattern, references)

# Fonction pour rechercher un article via l'API CrossRef
def search_crossref(title):
    url = "https://api.crossref.org/works"
    params = {"query.bibliographic": title, "rows": 1}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["message"]["items"]:
            article = data["message"]["items"][0]
            return article.get("DOI", "DOI introuvable"), article.get("title", ["Titre introuvable"])[0]
    return None, None

# Recherche des DOIs
for match in matches:
    authors, journal, year, volume, pages = match
    query = f"{authors}, {journal}, {year}, {volume}, {pages}"
    doi, found_title = search_crossref(query)
    print(f"Référence : {query}\nDOI : {doi}\nTitre trouvé : {found_title}\n")
