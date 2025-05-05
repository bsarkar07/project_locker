import pandas as pd

df = pd.read_csv("./resources/2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv")
print(df['Primary Fur Color'][:5])

# print(type(df))

furColor = df['Primary Fur Color'].tolist()

colorDict = dict()
for color in furColor:

    try:
        colorDict[color] += 1
    except:
        colorDict[color] = 0

df2 = pd.DataFrame(colorDict.items(), columns = ['Color', 'Count'])
df2.to_csv("./resources/color_count.csv", index = False)

