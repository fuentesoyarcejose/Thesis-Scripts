#generate a plot of posts (rows) per month

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

df = pd.read_csv("C:/Users/Jose Ignacio/Desktop/UNI/Mémoire/Data/final data/Data 202511/mergedfinal.csv")

df["creation_date"] = pd.to_datetime(df["creation_date"], utc = True)


post_per_week = df.resample('W', on='creation_date').size()
post_per_month = df.resample('M', on='creation_date').size()
post_per_year = df.resample('Y', on='creation_date').size()

full_month_index = pd.date_range(post_per_month.index.min(),
                                 post_per_month.index.max(),
                                 freq="M")

post_per_month=post_per_month.reindex(full_month_index,fill_value=0)


fig, ax =plt.subplots(figsize=(12,5))
ax.plot(post_per_month.index, post_per_month.values, marker='o', linestyle='-',
        color="lightblue", linewidth=2)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%Y'))
plt.xticks(rotation=45, ha='right')

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}".replace(",",".")))


for x,y in zip(post_per_month.index, post_per_month.values):
    ax.text(x,y + max(post_per_month.values)*0.02,
            f"{y:,}".replace(",","."),
            ha='center', va='bottom',fontsize= 8, color='black')


#adding a specific label to May and June to see the number of posts (they have a low number compared to average)

target_months = ["2025-04","2025-05"]

for target in target_months:
    p =pd.Period(target, freq="M")
    mask = post_per_month.index.to_period("M") == p
    if mask.any():
        x = post_per_month.index[mask][0]
        y = post_per_month[mask][0]
        ax.text(x,y + max(post_per_month.values)*0.02,
                f"{y:,}".replace(",","."),
                ha='center', va='bottom', fontsize=9, color='black',fontweight='bold')
        


plt.title("Number of posts per month")
plt.xlabel("Month")
plt.ylabel("N° of posts")
plt.tight_layout
plt.show()


#past the number of posts per month to a csv for future reference
posts_summary = post_per_month.reset_index()
posts_summary.columns=['month', 'n posts']

posts_summary['month'] = posts_summary['month'].dt.strftime('%m-%Y')
posts_summary.to_csv('C:/Users/Jose Ignacio/Desktop/UNI/Mémoire/Data/final data/Data 202511/posts_by_month.csv', index=False, sep=';')

print("done")
