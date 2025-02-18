from transformers import pipeline

# Charger le pipeline de résumé
#summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Utiliser un modèle plus léger
#summarizer = pipeline("summarization", model="distilbart-cnn-12-6")  # Modèle plus léger

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


# Texte à résumer
text = """
In our study of nanoparticle networks manipulated bysurrounding electrodes, key design features include the numberof nanoparticles (NNP) and the location and quantity of controlelectrodes (NC). Although we ﬁnd any possible two-input Booleanlogic function in the sampled phase space (see SupplementarySection S4), here we just focus on the six major Boolean logicgates AND, OR, XOR, NAND, NOR, and XNOR. In this section, weﬁrst analyze the dependence of logic gate ﬁtness (F) on the locationand number of control electrodes. Given the signiﬁcant impact ofelectrode positioning, the subsequent section addresses an increasein system size while considering two distinct electrode positioningsetups. All results are contextualized within the framework ofnonlinearproperties.Additionalinsightsintoparameterdependence on NNP and NC can be found in SupplementarySection S7; Supplementary Figure S8."""

# Résumer le texte
summary = summarizer(text, max_length=300, min_length=100, do_sample=False)

# Afficher le résumé
print(summary[0]['summary_text'])