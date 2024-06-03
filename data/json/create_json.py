# %%
import pandas as pd
import json

df = pd.read_excel("../Principal.xlsx").drop_duplicates()

# %%
df["Ubicación"].value_counts()
