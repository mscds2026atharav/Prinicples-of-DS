import pandas as pd

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
df=pd.read_csv("ball_by_ball_it20.csv")

#Top 3 teams and runs scored
print("=====Top 3 teams=====")
countries = df.groupby("Bat First", as_index=False)["Target Score"].max().sort_values(by="Target Score", ascending=False).reset_index(drop=True)

countries=countries.rename(columns={'Bat First' : 'Country'})
countries=countries.rename(columns={'Target Score' : 'Score'})

print(countries.head(3))
print()
#Top 5 batter and runs scored
print()
print("=====Top 5 batters=====")
batters=df.groupby("Batter", as_index=False)["Batter Runs"].sum().sort_values(by="Batter Runs",ascending=False).reset_index(drop=True)

batters=batters.rename(columns={'Batter Runs' : 'Overall Runs'})

print(batters.head(5))
print()
#Top 3 bowlers by wicket taken
print()
print("=====Top 3 bowlers=====")
bowlers=df.groupby("Bowler",as_index=False)["Wicket"].sum().sort_values(by="Wicket",ascending=False).reset_index(drop=True)

bowlers=bowlers.rename(columns={'Wicket' : 'Wickets'})

print(bowlers.head(3))
print()

#Get country-wise count for how many got bowled,caught,hit wicket,lbw,run out
topcountries=['Afghanistan','Australia','Canada','England','India','Ireland','Italy','Namibia','Nepal','Netherlands','New Zealand','Oman','Pakistan','Scotland','South Africa','Sri Lanka','United States of America','United Arab Emirates','West Indies','Zimbabwe']

applicable_outs=['caught','bowled','hit wicket','lbw','run out']

matrix=[[0]*len(topcountries) for _ in range(len(applicable_outs))]

outs_df=df[df["Method"].isin(applicable_outs) & df["Bat First"].isin(topcountries)]

columns = ["Method", "Bat First"]
outs_df = outs_df[columns]
outs_df["Method"] = outs_df["Method"].astype(str)
outs_df["Bat First"] = outs_df["Bat First"].astype(str)

for i in range(0, len(applicable_outs)):
    for j in range(0, len(topcountries)):
        for index, series in outs_df.iterrows():
            if series["Method"] == applicable_outs[i] and series["Bat First"] == topcountries[j]:
                matrix[i][j] = matrix[i][j] + 1

print("Get Country-wise count for how many got bowled, caught, hit wicket, lbw, run out")
print("{:<30}".format(""), end="")
for out in applicable_outs:
    print("{:<15}".format(out), end="")
print()

for j in range(len(topcountries)):
    print("{:<30}".format(topcountries[j]), end="")
    for i in range(len(applicable_outs)):
        print("{:<15}".format(matrix[i][j]), end="")
    print()


#plot line chart for years and runs
df['Date']=pd.to_datetime(df["Date"])
df['Date']=df['Date'].dt.year

years=df.groupby("Date",as_index=False)["Target Score"].max().reset_index(drop=True)
x=years["Date"]
y=years["Target Score"]

plt.subplot(1,2,1)
plt.plot(x,y,linewidth = '2.5',color="Black")

# Plot pie chart for displaying number of unique batters per country

battercount = df.groupby(
    'Bat First',
    as_index=False
)['Batter'].nunique()

battercount = battercount.rename(columns={
    "Bat First": "Country",
    "Batter": "Count"
})

battercount = battercount[
    battercount["Country"].isin(topcountries)
]

totalbatters = battercount["Count"].sum()

def my_autopct(pct):
    count = int(round(pct * totalbatters / 100))
    return f'{count}'


plt.subplot(1, 2, 2)

plt.pie(
    battercount["Count"],
    labels=battercount["Country"],
    autopct=my_autopct,
    startangle=90
)

plt.title("Number of Batters per Country")

plt.show()