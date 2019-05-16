import pandas as pd


t = pd.DataFrame([1,2,3])

for i,a in t.iterrows():
    print(i)
