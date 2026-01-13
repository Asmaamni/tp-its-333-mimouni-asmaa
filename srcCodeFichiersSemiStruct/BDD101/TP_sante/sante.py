import json

# Charger le fichier JSON
with open("sante.json", "r", encoding="utf-8") as f:
    personnes = json.load(f)

def chercher_parametres_sante(id_personne):
    # Convertir en chaîne pour être sûr
    id_personne = str(id_personne)
    
    if id_personne in personnes:
        return json.dumps(personnes[id_personne], indent=4, ensure_ascii=False)
    else:
        return json.dumps({"erreur": "Personne non trouvée"}, indent=4, ensure_ascii=False)

# Test avec ID existant
print(chercher_parametres_sante("3"))