
# BenÃ¶tigte Pakete importieren
import matplotlib.pyplot as plt
from matplotlib import pyplot
import geopandas
import descartes, geopandas as gpd
from shapely.geometry import Point, Polygon
from pyproj import Proj

import numpy as np, pandas as pd
import descartes, geopandas as gpd
import pandas
import matplotlib.pyplot as plt

import seaborn as sns
import pandas as pd

import statistics
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import pyplot



"""
Analyse auf Gemeindeebene
"""

# Shapefile Gemeindegrenzen inkl. Bevölkerungsdaten Stand 31.12.2015 einlesen
germany_map_gemeinde = gpd.read_file('GEM_2015_ew.shp')

# Mobilitätskennzahlen einlesen
mobility = pd.read_excel('small_area_estimation.xlsx',
                         sheet_name="Ergebnisse Gemeindeebene",
                         usecols=["AGS","Tageskilometer", "Anteil MIV-Fahrer-km"],
                         converters={'AGS': '{:0>8}'.format},  # Führende 0 hinzufügen
                         nrows=11306)

# RegioStaR7 Refernezdatei für den Gebietsstand 31.12.2015 einlesen
regiostar7 = pd.read_excel('regiostar-referenzdateien.xlsx',
                           sheet_name="ReferenzGebietsstand2015",
                           usecols=["gem", "RegioStaR7", "RegioStaR2"],
                           nrows=11167,
                           converters={'gem': '{:0>8}'.format})  # Führende 0 hinzufügen sodass gem=AGS

regiostar7.rename(columns={'gem': 'AGS'}, inplace=True)  # Unbenennen

"""
Die Einteilung der Gemeinden gemäß des RegioStar7 wird der shape file übergeben

Grundlage für die Zuordnung sind die AGS."

"""
merged = germany_map_gemeinde.merge(
    regiostar7, left_on="AGS", right_on="AGS", how="left"
)

"""
Die Mobilitätskennzahlen für jede Gemeinde werden dem dazugehörigen Kreis entnommen.

Bestandteile AGS: Bundesland (2 Stellen), Regierungsbezirk (1 Stelle), Kreis (2 Stellen) und Gemeinde (3 Stellen).
Kreiskennziffer: Bundesland (2 Stellen), Regierungsbezirk (1 Stelle), Kreis (2 Stellen)

Damit ist die KKZ ist in der AGS enthalten. Der Sachverhalt wird am Beispiel von Neuhardenberg  dargestellt:

AGS 12 0 64 340
12 Brandenburg
0 (in Brandenburg gibt es die Verwaltungseinheit Regierungsbezirk nicht)
64 Landkreis Märkisch-Oderland
340 Gemeinde Neuhardenberg


KKZ 12 0 64
12 Brandenburg
0 (in Brandenburg gibt es die Verwaltungseinheit Regierungsbezirk nicht)
64 Landkreis Märkisch-Oderland

Ausgehend von diesem Zusammenhang wurden die Mobilitätsergebnisse in der Excel gemäß der Kreiskennziffer den Gemeinden zugeordnet
Durch den Zwischenschritt in der Excel Datei lassen sich die Mobilitätsdaten anhand der AGS der shapefile zeilenweise anhängen
"""
df_energiebedarf = merged.merge(
    mobility, left_on="AGS", right_on="AGS", how="left"
)

"""
Ergebnis ist eine Tabelle mit der benötigten Datengrundlage zur Berechnung des Energiebedarfs.
Im nächsten Schritt wird der Energiebedarf modelliert.

"""
def add_energy_demand(Anteil_Antriebstechnologie,sce):
    result=df_energiebedarf
    # Anteil der Antriebstechnologie (Angabe des Kraftfahrtbundesamtes) * gesamte Tageskilometer (aus dem Small-Area-Verfahren) je Kreis * Anteil MIV-Fahrer-km (aus dem Small-Area-Verfahren) je Kreis * Bevölkerungsanzahl je Kreis * Kraftstoffverbrauch pro km 
    # Kraftstoffverbrauch Benzin [Liter] für den gesamten Kreis
    result['Kraftstoffbedarf Benzin [Liter]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[0].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * row['EWZ'] * 7.7/100
                                               ),
                                   axis=1,
                                   )

    # Kraftstoffverbrauch Benzin [Liter/Person] für den gesamten Kreis jedoch pro Person (im Bericht FC_i) 
    result['Kraftstoffbedarf Benzin [Liter/Person]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[0].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * 7.7/100
                                               ),
                                   axis=1,
                                   )
    
    # Kraftstoffverbrauch Benzin [Liter/a] Jahreswert! 
    result['Kraftstoffbedarf Benzin [Liter/a]'] = result.apply(lambda row:(row['Kraftstoffbedarf Benzin [Liter]'] * 365
                                               ),
                                   axis=1,
                                   )

    # Kraftstoffverbrauch Diesel [Liter]
    result['Kraftstoffbedarf Diesel [Liter]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[1].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * row['EWZ'] * 6.8/100
                                               ),
                                   axis=1,
                                   )

    # Kraftstoffverbrauch Diesel [Liter/Person] für den gesamten Kreis jedoch pro Person
    result['Kraftstoffbedarf Diesel [Liter/Person]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[1].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * 6.8/100
                                               ),
                                   axis=1,
                                   )
    
    # Kraftstoffverbrauch Diesel [Liter/a] Jahreswert! 
    result['Kraftstoffbedarf Diesel [Liter/a]'] = result.apply(lambda row:(row['Kraftstoffbedarf Diesel [Liter]'] * 365
                                               ),
                                   axis=1,
                                   )

    # Kraftstoffverbrauch Flüssiggas [Liter]
    result['Kraftstoffbedarf Flüssiggas [Liter]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[2].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * row['EWZ'] * 9.4/100
                                               ),
                                   axis=1,
                                   )

    # Kraftstoffverbrauch Flüssiggas [Liter/Person] für den gesamten Kreis jedoch pro Person
    result['Kraftstoffbedarf Flüssiggas [Liter/Person]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[2].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * 9.4/100
                                               ),
                                   axis=1,
                                   )
    
    # Kraftstoffverbrauch Flüssiggas [Liter/a] Jahreswert! 
    result['Kraftstoffbedarf Flüssiggas [Liter/a]'] = result.apply(lambda row:(row['Kraftstoffbedarf Flüssiggas [Liter]'] * 365
                                               ),
                                   axis=1,
                                   )

    # Kraftstoffverbrauch Hybrid [kWh]
    result['Kraftstoffbedarf Hybrid [kWh]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[3].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * row['EWZ'] * 55/100
                                               ),
                                   axis=1,
                                   )

    # Kraftstoffverbrauch Hybrid [kWh/Person] für den gesamten Kreis jedoch pro Person
    result['Kraftstoffbedarf Hybrid [kWh/Person]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[3].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * 55/100
                                               ),
                                   axis=1,
                                   )
    
    # Kraftstoffverbrauch Hybrid [kWh/a] Jahreswert! 
    result['Kraftstoffbedarf Hybrid [kWh/a]'] = result.apply(lambda row:(row['Kraftstoffbedarf Hybrid [kWh]'] * 365
                                               ),
                                   axis=1,
                                   )

    # Kraftstoffverbrauch Erdgas [kg]
    result['Kraftstoffbedarf Erdgas [kg]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[4].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * row['EWZ'] * 4.3/100
                                                ),
                                    axis=1,
                                    )

    # Kraftstoffverbrauch Erdgas [kg/Person] für den gesamten Kreis jedoch pro Person
    result['Kraftstoffbedarf Erdgas [kg/Person]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[4].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * 4.3/100
                                                ),
                                    axis=1,
                                    ) 
    
    # Kraftstoffverbrauch Erdgas [kg/a] Jahreswert! 
    result['Kraftstoffbedarf Erdgas [kg/a]'] = result.apply(lambda row:(row['Kraftstoffbedarf Erdgas [kg]'] * 365
                                               ),
                                   axis=1,
                                   )

    # Kraftstoffverbrauch Elektrofahrzeuge [kWh]
    result['Kraftstoffbedarf Elektrofahrzeuge [kWh]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[5].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * row['EWZ'] * 17/100
                                               ),
                                   axis=1,
                                   )

    # Kraftstoffverbrauch Elektrofahrzeuge [kWh/Person] für den gesamten Kreis jedoch pro Person
    result['Kraftstoffbedarf Elektrofahrzeuge [kWh/Person]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[5].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * 17/100
                                               ),
                                   axis=1,
                                   ) 
    
    # Kraftstoffverbrauch Elektrofahrzeuge [kWh/a] Jahreswert! 
    result['Kraftstoffbedarf Elektrofahrzeuge [kWh/a]'] = result.apply(lambda row:(row['Kraftstoffbedarf Elektrofahrzeuge [kWh]'] * 365
                                               ),
                                   axis=1,
                                   )
    
    # Kraftstoffverbrauch Wasserstofffahrzeuge [kg]
    result['Kraftstoffbedarf Wasserstofffahrzeuge [kg]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[6].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * row['EWZ'] * 0.8/100
                                                   ),
                                       axis=1,
                                       )

    # Kraftstoffverbrauch Wasserstofffahrzeuge [kg/Person] für den gesamten Kreis jedoch pro Person
    result['Kraftstoffbedarf Wasserstofffahrzeuge [kg/Person]'] = result.apply(lambda row:(df_Antriebstechnologien.loc[6].at[Anteil_Antriebstechnologie] * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 + sce) * 0.8/100
                                                   ),
                                       axis=1,
                                       ) 
    
    # Kraftstoffverbrauch Wasserstofffahrzeuge [kg/a] Jahreswert! 
    result['Kraftstoffbedarf Wasserstofffahrzeuge [kg/a]'] = result.apply(lambda row:(row['Kraftstoffbedarf Wasserstofffahrzeuge [kg]'] * 365
                                               ),
                                   axis=1,
                                   )
    
    # Energiebedraf Gemeindeeben Tank-to-Wheel TTW [MJ]
    result['Energiebedarf TTW [GJ]'] = result.apply(lambda row:((row['Kraftstoffbedarf Benzin [Liter]'] * 32 + row['Kraftstoffbedarf Diesel [Liter]'] * 35.7 +
                                                                                           row['Kraftstoffbedarf Flüssiggas [Liter]'] * 24.5 + row['Kraftstoffbedarf Hybrid [kWh]'] * 3.6 +
                                                                                           row['Kraftstoffbedarf Erdgas [kg]'] * 45.1 + row['Kraftstoffbedarf Elektrofahrzeuge [kWh]'] * 3.6 +
                                                                                           row['Kraftstoffbedarf Wasserstofffahrzeuge [kg]'] * 120) / 1000
                                               ),
                                   axis=1,
                                   )

    # Energiebedraf Gemeindeeben Tank-to-Wheel TTW [MJ/Person]
    result['Energiebedarf TTW [MJ/Person]'] = result.apply(lambda row:(row['Kraftstoffbedarf Benzin [Liter/Person]'] * 32 + row['Kraftstoffbedarf Diesel [Liter/Person]'] * 35.7 +
                                                                                       row['Kraftstoffbedarf Flüssiggas [Liter/Person]'] * 24.5 + row['Kraftstoffbedarf Hybrid [kWh/Person]'] * 3.6 +
                                                                                       row['Kraftstoffbedarf Erdgas [kg/Person]'] * 45.1 + row['Kraftstoffbedarf Elektrofahrzeuge [kWh/Person]'] * 3.6 +
                                                                                       row['Kraftstoffbedarf Wasserstofffahrzeuge [kg/Person]'] * 120
                                               ),
                                   axis=1,
                                   )
    return result

# Definition welches Szenario gewählt werden soll:
# Basis 2017: 0 %

# Referenzszenario 2030: - 5,8 %
# Kontrafaktisches Szenario 2030: 0 %
# Szenario der verstärkten Automatisierung 2030: - 9,8 %
# Verkehrsprognose 2030: + 2,6 %

# Referenzszenario 2050: + 5,556 %
# Szenario „neue Individualmobilität“ (NIM) 2050: - 3,968 %
# Szenario „neue Dienstleistungen“ (NDL) 2050: - 39,68 %
# Szenario „neue Mobilitätskultur“ (NMK) 2050: -71,43 %

# sce = 0 #-0.058

# DataFrame mit unterschiedlichen Anteilen der Antriebstechnologien für 2017, 2030 und 2050
# Benzin, Diesel, Flüssiggas, Hybrid, Erdgas, Elektro, Wasserstoff

d={'2017':[0.662, 0.322, 0.011, 0.0029, 0.002, 0.00057, 0], 
   'TN Strom 2030':[0.4118, 0.3224, 0.006, 0.08, 0.0011, 0.1788, 0], 'TN Strom 2050':[0.0623, 0.015, 0, 0.1047, 0, 0.773, 0.045],
   'TN PtG-PtL 2030':[0.4212, 0.3953, 0.006, 0.0588, 0.0011, 0.1176, 0], 'TN PtG-PtL 2050':[0.3251, 0.1216, 0, 0.2233, 0, 0.2978, 0.0323],
   'TN H2 2030':[0.442, 0.3641, 0.006, 0.0426, 0.0011, 0.1442, 0], 'TN H2 2050':[0.1022, 0.0324, 0, 0.0249, 0, 0.5985, 0.2419]}
df_Antriebstechnologien=pd.DataFrame(data=d)

# Anteil_Antriebstechnologie = '2017'

# Pfad definieren:
path = '//rdhraid/users$/jrieck/Desktop/Python/FNR/Modell/results/0_2017/'

# add_energy_demand(Anteil_Antriebstechnologie,sce)
df_energiebedarf_sce = add_energy_demand('2017', 0)
df_energiebedarf_sce.to_csv(path+'energiebedarf.csv',index=False)  



"""
Einbindung der Daten aus dem Jericho-E Modell um temporäre profile zu erhalten
"""
df_profile = pd.read_excel('nuts2_hourly_service_Pas_km.xlsx', 
                           sheet_name="share",
                           nrows=8761)

# df_temp_benzin = df_temp_benzin.apply(lambda row:(0.00057 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km']*row['EWZ'] * 17/100
#                                                ),
#                                    axis=0,
#                                    )

# energy_type = 'Kraftstoffbedarf Benzin [Liter]' , 'Kraftstoffbedarf Diesel [Liter]' ,
# 'Kraftstoffbedarf Flüssiggas [Liter]' , 'Kraftstoffbedarf Hybrid [kWh]' ,
# 'Kraftstoffbedarf Erdgas [kg]' , 'Kraftstoffbedarf Elektrofahrzeuge [kWh]', 
# 'Kraftstoffbedarf Wasserstofffahrzeuge [kg]'
def add_tempral_profile(energy_type):
    result=pd.DataFrame(index=range(len(df_profile['DE11'])),columns=range(len(df_energiebedarf['OBJECTID'])))
    result.columns=df_energiebedarf['OBJECTID']
    i=0
    while i < len(df_energiebedarf_sce['NUTS']) :
        t=df_energiebedarf_sce.loc[i].at['NUTS']
        t=t[:-1]
        result[i+1]= df_energiebedarf_sce.loc[i].at[energy_type] * df_profile[t]
        i = i + 1
    return result

df_profile_Antrieb_sce = add_tempral_profile('Kraftstoffbedarf Benzin [Liter/a]') 
df_profile_Antrieb_sce.to_csv(path+'profile_Benzin.csv',index=False)  
del df_profile_Antrieb_sce

df_profile_Antrieb_sce = add_tempral_profile('Kraftstoffbedarf Diesel [Liter/a]') 
df_profile_Antrieb_sce.to_csv(path+'profile_Diesel.csv',index=False)  
del df_profile_Antrieb_sce

df_profile_Antrieb_sce = add_tempral_profile('Kraftstoffbedarf Flüssiggas [Liter/a]') 
df_profile_Antrieb_sce.to_csv(path+'profile_LNG.csv',index=False)  
del df_profile_Antrieb_sce

df_profile_Antrieb_sce = add_tempral_profile('Kraftstoffbedarf Hybrid [kWh/a]') 
df_profile_Antrieb_sce.to_csv(path+'profile_Hybrid.csv',index=False)  
del df_profile_Antrieb_sce

df_profile_Antrieb_sce = add_tempral_profile('Kraftstoffbedarf Erdgas [kg/a]') 
df_profile_Antrieb_sce.to_csv(path+'profile_Erdgas.csv',index=False)  
del df_profile_Antrieb_sce

df_profile_Antrieb_sce = add_tempral_profile('Kraftstoffbedarf Elektrofahrzeuge [kWh/a]') 
df_profile_Antrieb_sce.to_csv(path+'profile_Elektro.csv',index=False)  
del df_profile_Antrieb_sce

df_profile_Antrieb_sce = add_tempral_profile('Kraftstoffbedarf Wasserstofffahrzeuge [kg/a]') 
df_profile_Antrieb_sce.to_csv(path+'profile_Wasserstoff.csv',index=False)  
del df_profile_Antrieb_sce
    

"""

Grafische Analyse der Ergebnisse

"""

# Energiebedarf [MJ/Person]
# Plotten
fig, ax = plt.subplots(1, figsize=(15,15))
df_energiebedarf_sce.to_crs(epsg=4326).plot(
    ax=ax,
    column="Energiebedarf TTW [MJ/Person]", 
    cmap = 'rainbow',  
    )

# Skala bestimmen
vmin, vmax = df_energiebedarf_sce["Energiebedarf TTW [MJ/Person]"].min(), df_energiebedarf_sce["Energiebedarf TTW [MJ/Person]"].max()

#Achsen entfernen
ax.axis('off')

# Titel hinzufügen
ax.set_title('TTW-Energiebedarf [MJ/Person] - Gemeindeebene', fontdict={'fontsize': '25', 'fontweight' : '3'})

# Quellen hinzufügen
ax.annotate('Quelle: Eigene Auswertungen auf Grundlage von Regionalisierungsergebnissen des MiD 2017 (BMVI) ',xy=(0.1, .08), xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')

# Legende hinzufügen
sm = plt.cm.ScalarMappable(cmap = 'rainbow', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []

# Legende hinzufügen
cbar = fig.colorbar(sm)

#Speichern /Users/jenny/Documents
plt.savefig(path+'Energiebedarf TTW [MJ_Person]')




"""
grafische Analyse der Ergebnisse auf Kreisebene: Tank-to-Wheel Energiebedarf auf Kreisebene [MJ]
"""
# Tank-to-Wheel Energiebedarf in [GJ]
# Plotten
fig, ax = plt.subplots(1, figsize=(15,15))
df_energiebedarf_sce.to_crs(epsg=4326).plot(
    ax=ax,
    column="Energiebedarf TTW [GJ]", 
    cmap = 'rainbow',
    )

# Skala bestimmen
vmin, vmax = df_energiebedarf_sce["Energiebedarf TTW [GJ]"].min(), df_energiebedarf_sce["Energiebedarf TTW [GJ]"].max()

#Achsen entfernen
ax.axis('off')

# Titel hinzufügen
ax.set_title('Tank-to-Wheel Energiebedarf [GJ] - Gemeindeebene', fontdict={'fontsize': '25', 'fontweight' : '3'})

# Quellen hinzufügen
ax.annotate('Quelle: Eigene Auswertungen auf Grundlage von Regionalisierungsergebnissen des MiD 2017 (BMVI) ',xy=(0.1, .08), xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')

# Legende hinzufügen
sm = plt.cm.ScalarMappable(cmap = 'rainbow', norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []

# Legende hinzufügen
cbar = fig.colorbar(sm)

#Speichern
plt.savefig(path+'Tank-to-Wheel Energiebedarf [GJ] - Kreisebene - 1')



#mit Scheme "Quantiles"

# Tank-to-Wheel Energiebedarf in [GJ]
# Plotten
fig, ax = plt.subplots(1, figsize=(15,15))
df_energiebedarf_sce.to_crs(epsg=4326).plot(
    ax=ax,
    column="Energiebedarf TTW [GJ]", 
    cmap = 'rainbow',
    scheme='quantiles',
    k=10,#Anzahl Intervalle
    legend=True
    )

# Skala bestimmen
vmin, vmax = df_energiebedarf_sce["Energiebedarf TTW [GJ]"].min(), df_energiebedarf_sce["Energiebedarf TTW [GJ]"].max()

#Achsen entfernen
ax.axis('off')

# Titel hinzufügen
ax.set_title('Tank-to-Wheel Energiebedarf [GJ] - Gemeindeebene', fontdict={'fontsize': '25', 'fontweight' : '3'})

# Quellen hinzufügen
ax.annotate('Quelle: Eigene Auswertungen auf Grundlage von Regionalisierungsergebnissen des MiD 2017 (BMVI) ',xy=(0.1, .08), xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')

#Speichern
plt.savefig(path+'Tank-to-Wheel Energiebedarf [GJ] - Kreisebene - 2')



# Ausblenden von städtischen Räumen nach RegioStaR2
df_filtered_map= df_energiebedarf_sce[df_energiebedarf['RegioStaR2']>1] 

fig, ax = plt.subplots(1, figsize=(15,15))
df_filtered_map.to_crs(epsg=4326).plot(
    ax=ax,
    column="Energiebedarf TTW [GJ]", 
    cmap = 'rainbow',
    scheme='quantiles',
    legend=True,
    k=15
     )
#Achsen entfernen
ax.axis('off')
# Titel hinzufügen
ax.set_title('TTW-Energiebedarf in GJ ländlicher Regionen', fontdict={'fontsize': '25', 'fontweight' : '3'})
# Quellen hinzufügen
ax.annotate('Quelle: Eigene Auswertungen auf Grundlage von Regionalisierungsergebnissen des MiD 2017 (BMVI) ',xy=(0.1, .08), xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
#Speichern
plt.savefig(path+'TTW-Energiebedarf in GJ ländlicher Regionen gemäß RegioStaR2')


# nicht mehr genutzt:
    # """
    # Einbindung der Szenarien für 2030 und 2050
    # in Bearbeitung:
    # """
    # # Definition welches Senario gewählt werden soll:
    # sce = 0.058
    # df_Referenz_2030=pd.DataFrame(index=df_energiebedarf['OBJECTID'])   
    # # Anteil der Antriebstechnologie (Angabe des Kraftfahrtbundesamtes) * gesamte Tageskilometer (aus dem Samll-Area-Verfahren) je Kreis * Anteil MIV-Fahrer-km (aus dem Samll-Area-Verfahren) je Kreis * Bevölkerungsanzahl je Kreis * Kraftstoffverbrauch pro km 
    # # Kraftstoffverbrauch Benzin [Liter] für den gesamten Kreis
    # df_Referenz_2030['Kraftstoffbedarf Benzin [Liter]'] = df_energiebedarf.apply(lambda row:(0.4051 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * row['EWZ'] * 7.7/100
    #                                                ),
    #                                    axis=1,
    #                                    )

    # # Kraftstoffverbrauch Benzin [Liter/Person] für den gesamten Kreis jedoch pro Person (im Bericht FC_i) 
    # df_Referenz_2030['Kraftstoffbedarf Benzin [Liter/Person]'] = df_energiebedarf.apply(lambda row:(0.4051 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * 7.7/100
    #                                                ),
    #                                    axis=1,
    #                                    )

    # # Kraftstoffverbrauch Diesel [Liter]
    # df_Referenz_2030['Kraftstoffbedarf Diesel [Liter]'] = df_energiebedarf.apply(lambda row:(0.197 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * row['EWZ'] * 6.8/100
    #                                                ),
    #                                    axis=1,
    #                                    )

    # # Kraftstoffverbrauch Diesel [Liter/Person] für den gesamten Kreis jedoch pro Person
    # df_Referenz_2030['Kraftstoffbedarf Diesel [Liter/Person]'] = df_energiebedarf.apply(lambda row:(0.197 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * 6.8/100
    #                                                ),
    #                                    axis=1,
    #                                    )

    # # Kraftstoffverbrauch Flüssiggas [Liter]
    # df_Referenz_2030['Kraftstoffbedarf Flüssiggas [Liter]'] = df_energiebedarf.apply(lambda row:(0.0067 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * row['EWZ'] * 9.4/100
    #                                                ),
    #                                    axis=1,
    #                                    )

    # # Kraftstoffverbrauch Flüssiggas [Liter/Person] für den gesamten Kreis jedoch pro Person
    # df_Referenz_2030['Kraftstoffbedarf Flüssiggas [Liter/Person]'] = df_energiebedarf.apply(lambda row:(0.0067 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * 9.4/100
    #                                                ),
    #                                    axis=1,
    #                                    )

    # # Kraftstoffverbrauch Hybrid [kWh]
    # df_Referenz_2030['Kraftstoffbedarf Hybrid [kWh]'] = df_energiebedarf.apply(lambda row:(0.11 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * row['EWZ'] * 55/100
    #                                                ),
    #                                    axis=1,
    #                                    )

    # # Kraftstoffverbrauch Hybrid [kWh/Person] für den gesamten Kreis jedoch pro Person
    # df_Referenz_2030['Kraftstoffbedarf Hybrid [kWh/Person]'] = df_energiebedarf.apply(lambda row:(0.11 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * 55/100
    #                                                ),
    #                                    axis=1,
    #                                    )

    # # Kraftstoffverbrauch Erdgas [kg]
    # df_Referenz_2030['Kraftstoffbedarf Erdgas [kg]'] = df_energiebedarf.apply(lambda row:(0.0012 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * row['EWZ'] * 4.3/100
    #                                                 ),
    #                                     axis=1,
    #                                     )

    # # Kraftstoffverbrauch Erdgas [kg/Person] für den gesamten Kreis jedoch pro Person
    # df_Referenz_2030['Kraftstoffbedarf Erdgas [kg/Person]'] = df_energiebedarf.apply(lambda row:(0.0012 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * 4.3/100
    #                                                 ),
    #                                     axis=1,
    #                                     ) 

    # # Kraftstoffverbrauch Elektrofahrzeuge [kWh]
    # df_Referenz_2030['Kraftstoffbedarf Elektrofahrzeuge [kWh]'] = df_energiebedarf.apply(lambda row:(0.27 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * row['EWZ'] * 17/100
    #                                                ),
    #                                    axis=1,
    #                                    )

    # # Kraftstoffverbrauch Elektrofahrzeuge [kWh/Person] für den gesamten Kreis jedoch pro Person
    # df_Referenz_2030['Kraftstoffbedarf Elektrofahrzeuge [kWh/Person]'] = df_energiebedarf.apply(lambda row:(0.27 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * 17/100
    #                                                ),
    #                                    axis=1,
    #                                    )  

    # # Kraftstoffverbrauch Wasserstofffahrzeuge [kWh]
    # df_Referenz_2030['Kraftstoffbedarf Wasserstofffahrzeuge [kg]'] = df_energiebedarf.apply(lambda row:(0.001 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * row['EWZ'] * 0.8/100
    #                                                ),
    #                                    axis=1,
    #                                    )

    # # Kraftstoffverbrauch Wasserstofffahrzeuge [kWh/Person] für den gesamten Kreis jedoch pro Person
    # df_Referenz_2030['Kraftstoffbedarf Wasserstofffahrzeuge [kg/Person]'] = df_energiebedarf.apply(lambda row:(0.001 * row["Tageskilometer"] * row['Anteil MIV-Fahrer-km'] * (1 - sce) * 0.8/100
    #                                                ),
    #                                    axis=1,
    #                                    )  
