import pandas as pd
pd.set_option("display.width", 200)

jalons = pd.read_csv("data/jalons.csv")
print(jalons)

commandes = pd.read_csv("data/commandes.csv")
print(commandes)
