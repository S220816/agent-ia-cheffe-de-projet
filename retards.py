import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

commandes = pd.read_csv("data/commandes.csv")
commandes["date_prevue"] = pd.to_datetime(commandes["date_prevue"])
commandes["date_reelle"] = pd.to_datetime(commandes["date_reelle"])
commandes["retard_jours"] = (commandes["date_reelle"] - commandes["date_prevue"]).dt.days

print(commandes[["id", "fournisseur", "jalon_id", "retard_jours"]])
