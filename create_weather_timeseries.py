import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

REL_PATH_TO_DWD_CDC_WEATHER_DATA = "produkt_tu_stunde_kurz.txt"
SEPARATOR = ";"
TEMP_COL = "TT_TU"
TIME_COL = "MESS_DATUM"
UPPER_QUANTILE = 0.95git
LOWER_QUANTILE = 0.05
OUTPUT_DATA_PATH= "processed_weather_data.csv"
OUTPUT_SEPARATOR = ","

# Find quantiles in this timespan
# YYYYMMDDHH
T_WINDOW = [2015 * 1e6, 2021 * 1e6]

# Analyze these years
YEARS = [2018, 2019]
# With these months
# MMDDHH as int, strip leading 0
START_TIME = 50100
END_TIME = 63100



# Read data
df = pd.read_csv(REL_PATH_TO_DWD_CDC_WEATHER_DATA, sep=SEPARATOR)
df = df.loc[(df[TIME_COL] > T_WINDOW[0]) & (df[TIME_COL] < T_WINDOW[1])]
df = df.loc[df[TEMP_COL] != - 999]
# Find quantiles
high_quantil_temp_all_data = df[TEMP_COL].quantile(q=UPPER_QUANTILE)
low_quantil_temp_all_data = df[TEMP_COL].quantile(q=LOWER_QUANTILE)
print("Low Quantile: " , low_quantil_temp_all_data, "\t \t High Quantile: ", high_quantil_temp_all_data)
df_uncut = df.copy()
# Cap data to quantiles
df.loc[df[TEMP_COL] > high_quantil_temp_all_data, TEMP_COL] = high_quantil_temp_all_data
df.loc[df[TEMP_COL] < low_quantil_temp_all_data, TEMP_COL] = low_quantil_temp_all_data

df_tw = pd.DataFrame()
df_uncut_tw = pd.DataFrame()
for year in YEARS:
    year_start_time = year * 1e6 + START_TIME
    year_end_time = year * 1e6 + END_TIME
    if year_end_time < year_start_time: year_end_time = year_end_time + 1e6
    new_df = df.loc[(df[TIME_COL] >= year_start_time) &
                    (df[TIME_COL] < year_end_time)].copy()
    df_tw = pd.concat((df_tw, new_df))
    new_df = df_uncut.loc[(df_uncut[TIME_COL] >= year_start_time) &
                          (df_uncut[TIME_COL] < year_end_time)].copy()
    df_uncut_tw = pd.concat((df_uncut_tw, new_df))

hours = []
temps_low = []
temps_high = []
temps_median = []

for h in range(0, 24):
    hour_temps = df_tw.loc[df_tw[TIME_COL] % 100 == h]
    temps_low.append(hour_temps[TEMP_COL].min())
    temps_high.append(hour_temps[TEMP_COL].max())
    temps_median.append(hour_temps[TEMP_COL].median())
    hours.append(h)
days = []
df_tw.reset_index(inplace=True)
i = 0
while i+23 < len(df_uncut_tw):
    while (abs(df_uncut_tw.iloc[i][TIME_COL]) % 100 != 0) and \
            (abs(df_uncut_tw.iloc[i+23][TIME_COL]) % 100 != 23):
        # Weak filter for only whole day data. has to start with 0 and end with 23
        # Special cases possible, where multiple days are seen as one. Skipped / Filtered data
        # still had an impact on above calculations of min max and median
        i += 1
    day = df_uncut_tw.iloc[i:i + 24]
    days.append(day[TEMP_COL].to_list())
    i += 24
out_df = pd.DataFrame(zip(hours, temps_low, temps_high, temps_median), index=hours,
                      columns=["Hour", "Lowest Temperature",
                               "Highest Temperature", "Median Temperature"]).set_index("Hour")
out_df.round(3).to_csv(OUTPUT_DATA_PATH, sep=OUTPUT_SEPARATOR)
df_days = pd.DataFrame(days).transpose()
a=df_days.plot()
out_df.plot(ylim=(a.axes.get_ylim()))

plt.show()



