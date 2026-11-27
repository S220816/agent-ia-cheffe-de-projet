import pandas as pd

AUJOURDHUI = pd.Timestamp("2027-03-20")

jalons = pd.read_csv("data/jalons.csv", parse_dates=["date_prevue"])
commandes = pd.read_csv("data/commandes.csv", parse_dates=["date_prevue", "date_reelle"])
ofs = pd.read_csv("data/ordres_fabrication.csv", parse_dates=["debut_prevu", "fin_prevue"])


def arrivee(c):
    if pd.notna(c["date_reelle"]):
        return c["date_reelle"]
    return max(c["date_prevue"], AUJOURDHUI)


def analyser_jalon(jalon_id):
    jalon = jalons[jalons["id"] == jalon_id].iloc[0]
    of = ofs[ofs["jalon_id"] == jalon_id].iloc[0]
    cmd = commandes[commandes["jalon_id"] == jalon_id]

    arrivees = cmd.apply(arrivee, axis=1)
    derniere = arrivees.max()
    bloquante = cmd.loc[arrivees.idxmax(), "id"]

    debut = max(of["debut_prevu"], derniere)
    fin = debut + (of["fin_prevue"] - of["debut_prevu"])
    marge = (jalon["date_prevue"] - fin).days
    etat = "MENACE" if marge < 0 else "sous controle"

    print(f"{jalon_id} ({jalon['nom']}) : commandes {list(cmd['id'])}")
    print(f"   dernier composant : {bloquante} le {derniere.date()}")
    print(f"   fabrication {of['id']} : {debut.date()} -> {fin.date()}")
    print(f"   marge {marge} j -> {etat}")


for jalon_id in ofs["jalon_id"]:
    analyser_jalon(jalon_id)
