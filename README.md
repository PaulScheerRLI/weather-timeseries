# weather-timeseries
A short script to create an hourly temperature timeseries from weather data from the cdc
This script outputs the upper and lower bounds for given data, specifically the cdc air temperature data  
https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/recent/  
Station-Ids can be found here  
https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/recent/TU_Terminwerte_Beschreibung_Stationen.txt  

After definining the years to analyze upper and lower quantiles, the timeperiods are defined from which data is extracted. Data above and below the found quantiles is
clipped to the upper and lower quantile values. The output is a .csv file with hourly temperatures of these clipped values with a column for min. values, max. values, and median values.
The results are plotted with all the analyzed daily data without clipping as well (filtered for days which have data for 24h).  

![Output](https://user-images.githubusercontent.com/104760879/197481920-5120eb04-7965-4538-a36c-4c48a2a44e63.png)
![Analyzed days without clipping](https://user-images.githubusercontent.com/104760879/197481908-02fe141b-686b-4a1b-9619-9f8da45101ea.png)
