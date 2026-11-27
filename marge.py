import pandas as pd

AUJOURDHUI = pd.Timestamp("2027-03-20")

jalons = pd.read_csv("data/jalons.csv", parse_dates=["date_prevue"])
commandes = pd.read_csv("data/commandes.csv", parse_dates=["date_prevue", "date_reelle"])
ofs = pd.read_csv("data/ordres_fabrication.csv", parse_dates=["debut_prevu", "fin_prevue"])


def analyser(commande_id):
    c = commandes[commandes["id"] == commande_id].iloc[0]

    # Date d'arrivee retenue
    if pd.notna(c["date_reelle"]):
        arrivee = c["date_reelle"]
        hypothese = "livree"
    else:
        arrivee = max(c["date_prevue"], AUJOURDHUI)
        hypothese = "pas livree, arrivee supposee"

    of = ofs[ofs["jalon_id"] == c["jalon_id"]].iloc[0]
    jalon = jalons[jalons["id"] == c["jalon_id"]].iloc[0]

    debut = max(of["debut_prevu"], arrivee)
    fin = debut + (of["fin_prevue"] - of["debut_prevu"])
    marge = (jalon["date_prevue"] - fin).days
    etat = "MENACE" if marge < 0 else "sous controle"

    print(f"{commande_id} ({hypothese} le {arrivee.date()}) -> {of['id']} -> {jalon['id']} : marge {marge} j -> {etat}")


for commande_id in commandes["id"]:
    analyser(commande_id)
