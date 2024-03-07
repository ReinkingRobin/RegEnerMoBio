#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 13:41:29 2024

@author: robinreinking
"""

#!/usr/bin/python3

from tkinter import *
from tkinter import scrolledtext
from scipy.spatial import KDTree
import numpy as np
import pandas as pd
import subprocess
import threading
from BiogasPlant import BiogasPlant
from BiogasUpgradingPlant import BiogasUpgradingPlant
from SteamReformer import SteamReformer
from FischerTropschSynthesis import FischerTropschSynthesis
import PARAMETER
import SQLiteBiogasPlant
import sys



data_new = pd.read_csv('Input.csv',delimiter=';',decimal=",") 

insallierte_leistung = np.array(data_new['Installierte Leistung'].tolist())
Anteil_getreide = np.array(data_new['Getreide'].tolist())
Anteil_guelle = np.array(data_new['Guelle'].tolist())
Anteil_Mist = np.array(data_new['Mist'].tolist())
Anlage_nummer = np.array(data_new['Anlage'].tolist())

data = np.stack((Anteil_guelle,Anteil_Mist,Anteil_getreide),axis=1)

#data= np.random.rand(10510,3)



fields = ('Anteil Gülle [in %]', 'Anteil Mist [in %]', 'Anteil Getreide [in %]','Ähnlichste Anlage','Fläche Silomais [in ha]','Fläche Winterroggen (GPS) [in ha]','Fläche Getreide [in ha]','Fläche Zwischenfrucht Gras [in ha]','Fläche Zwischenfrucht Senf [in ha]','Jahresbedarf CNG [in kg]','Jahresbedarf H2 [in kg]')



class ConsoleToGuiApp:
    def __init__(self, master):
        self.master = master
        master.title("Economy of Biogasplant")

        # Create a scrolled text widget to display console output
        self.text_widget = scrolledtext.ScrolledText(master, wrap=WORD, width=100, height=40)
        self.text_widget.grid(row=0, column=2, sticky=NSEW)

        # Redirect the console output to the text widget
        sys.stdout = self

        # Bind the closing event to the destroy method
        master.protocol("WM_DELETE_WINDOW", self.destroy)

    def write(self, text):
        """Write method to redirect console output to the text widget."""
        if self.text_widget:
            self.text_widget.insert(END, text)
            self.text_widget.see(END)  # Scroll to the end to always show the latest output

    def flush(self):
        """Flush method to fulfill the requirements of sys.stdout."""
        pass

    def destroy(self):
        """Override the destroy method to restore the original sys.stdout."""
        sys.stdout = sys.__stdout__
        self.master.destroy()



def final_balance(entries):
   # principal loan:
   #gesamt_masse = float(entries['Installierte Leistung [in kW]'].get())
   anteil_guelle =  float(entries['Anteil Gülle [in %]'].get()) 
   anteil_mist =  float(entries['Anteil Mist [in %]'].get())
   anteil_getreide =  float(entries['Anteil Getreide [in %]'].get()) 

   sample= np.array([anteil_guelle,anteil_mist,anteil_getreide])
   kdtree=KDTree(data)
   dist,points=kdtree.query(sample,1)
   Anlage_gewaehlt = Anlage_nummer[points].tolist()
   entries['Ähnlichste Anlage'].delete(0,END)
   entries['Ähnlichste Anlage'].insert(0,Anlage_gewaehlt)
   result(Anlage_gewaehlt,points)
   
def jahres_bedarf(entries):
   # principal loan:
   #gesamt_masse = float(entries['Installierte Leistung [in kW]'].get())
   flaeche_mais =  float(entries['Fläche Silomais [in ha]'].get()) 
   flaeche_roggen =  float(entries['Fläche Winterroggen (GPS) [in ha]'].get())
   flaeche_getreide =  float(entries['Fläche Getreide [in ha]'].get()) 
   flaeche_gras =  float(entries['Fläche Zwischenfrucht Gras [in ha]'].get())
   flaeche_senf =  float(entries['Fläche Zwischenfrucht Senf [in ha]'].get()) 
   
   Jahresbedarf_CNG = 9125 + flaeche_mais * 88.65 + flaeche_roggen * 64.93 + flaeche_getreide * 45.67 + flaeche_gras * 34.11 + flaeche_senf * 17.59
   Jahresbedarf_H2 = Jahresbedarf_CNG*0.4
   
   entries['Jahresbedarf CNG [in kg]'].delete(0,END)
   entries['Jahresbedarf CNG [in kg]'].insert(0,Jahresbedarf_CNG)
   entries['Jahresbedarf H2 [in kg]'].delete(0,END)
   entries['Jahresbedarf H2 [in kg]'].insert(0,Jahresbedarf_H2)

   

   
   
   
   
   
def result(Anlage_gewaehlt,points):   
   # define reference plant
   # 1, 3, 4, 6, 8 - 11, 14, 16, 18, 22, 27-29, 31, 33, 35, 37, 40, 42, 42, 47, 48, 51, 52, 54, 56, 57, 59
   bp11 = SQLiteBiogasPlant.set_biogas_plant(Anlage_gewaehlt)
   biogas_production = bp11.get_total_biogas()
   methane_production = bp11.get_total_methane()
   
   leistung=insallierte_leistung[points].tolist()
   Guelle=Anteil_guelle[points].tolist()
   Mist=Anteil_Mist[points].tolist()
   Getreide=Anteil_getreide[points].tolist()
   print("Biogas plant:")
   print(f"Biogas production = {biogas_production} m³/a")
   print(f"Methane production = {methane_production} m³/a")
   print(f"Installed Capacity = {leistung} kW")
   print(f"Share of wet manure = {Guelle} %")
   print(f"Share of dry manure = {Mist} %")
   print(f"Share of crop= {Getreide} %")
   

   # upgrading methods
   amine_scrubbing = BiogasUpgradingPlant(BiogasPlant=bp11, name="AS")
   membrane_1 = BiogasUpgradingPlant(BiogasPlant=bp11, name="M1")
   membrane_2 = BiogasUpgradingPlant(BiogasPlant=bp11, name="M2")
   pws = BiogasUpgradingPlant(BiogasPlant=bp11, name="PWS")
   pgs = BiogasUpgradingPlant(BiogasPlant=bp11, name ="PGS")
   psa = BiogasUpgradingPlant(BiogasPlant=bp11, name="PSA")
   print("\nUpgrading Methods:")
   print(f"Amine Scrubbing Biomethane flow = {amine_scrubbing.get_biomethane()} m³/a")
   print(f"Membrane 1 Biomethane flow = {membrane_1.get_biomethane()} m³/a")
   print(f"Membrane 2 Biomethane flow = {membrane_2.get_biomethane()} m³/a")
   print(f"Pressurized Waser Scrubbing Biomethane flow = {pws.get_biomethane()} m³/a")
   print(f"Polyethylene Glycol Scrubbing Biomethane flow = {pgs.get_biomethane()} m³/a")
   print(f"Pressure Swing Adsorption Biomethane flow = {psa.get_biomethane()} m³/a")

   # steam reforming
   steam_reforming = SteamReformer(BiogasPlant=bp11, main_substrate="corn")
   print("\nSteam Reforming:")
   print(f"Hydrogen Flow = {steam_reforming.get_hydrogen_flow()} m³/a")
   print(f"Hydrogen Mass = {steam_reforming.get_hydrogen_mass()} kg/d")

   # fischer-tropsch synthesis
   fischer_tropsch = FischerTropschSynthesis(BiogasPlant=bp11)
   print("\nFischer-Tropsch Synthesis:")
   print(f"Liquid Fuel production = {fischer_tropsch.get_sf_volume()} m³/a")

   # economic BP11
   print("\nEconomy Biogas Plant:")
   print(f"Biogas provision costs = {bp11.get_provision_costs()} €/a")
   print(f"Biogas provision costs without heating = {bp11.get_provision_costs_without_heating()} €/a")

   # economic biogas upgrading
   print("\nCosts Biogas Upgrading:")
   print(f"Amine Scrubbing costs = {amine_scrubbing.get_total_costs()} €/a")
   print(f"Membrane 1 costs = {membrane_1.get_total_costs()} €/a")
   print(f"Membrane 2 costs = {membrane_2.get_total_costs()} €/a")
   print(f"Pressurized Waser Scrubbing costs = {pws.get_total_costs()} €/a")
   print(f"Polyethylene Glycol Scrubbing costs = {pgs.get_total_costs()} €/a")
   print(f"Pressure Swing Adsorption costs = {psa.get_total_costs()} €/a")
   print("\nRevenue Biogas Upgrading:")
   print(f"Amine Scrubbing revenue with quota = {amine_scrubbing.get_total_revenue_quota()} €/a")
   print(f"Membrane 1 revenue with quota = {membrane_1.get_total_revenue_quota()} €/a")
   print(f"Membrane 2 revenue with quota = {membrane_2.get_total_revenue_quota()} €/a")
   print(f"Pressurized Waser Scrubbing revenue with quota = {pws.get_total_revenue_quota()} €/a")
   print(f"Polyethylene Glycol Scrubbing revenue with quota = {pgs.get_total_revenue_quota()} €/a")
   print(f"Pressure Swing Adsorption revenue with quota = {psa.get_total_revenue_quota()} €/a")
   print(f"Amine Scrubbing revenue concessionary taxes = {amine_scrubbing.get_total_revenue_taxes()} €/a")
   print(f"Membrane 1 revenue concessionary taxes = {membrane_1.get_total_revenue_taxes()} €/a")
   print(f"Membrane 2 revenue concessionary taxes = {membrane_2.get_total_revenue_taxes()} €/a")
   print(f"Pressurized Waser Scrubbing revenue concessionary taxes = {pws.get_total_revenue_taxes()} €/a")
   print(f"Polyethylene Glycol Scrubbing revenue concessionary taxes = {pgs.get_total_revenue_taxes()} €/a")
   print(f"Pressure Swing Adsorption revenue concessionary taxes = {psa.get_total_revenue_taxes()} €/a")
   print("\nBalance Biogas Upgrading:")
   print(f"Amine Scrubbing balance with quota = {amine_scrubbing.get_total_revenue_quota()-amine_scrubbing.get_total_costs()} €/a")
   print(f"Membrane 1 balance with quota = {membrane_1.get_total_revenue_quota()-membrane_1.get_total_costs()} €/a")
   print(f"Membrane 2 balance with quota = {membrane_2.get_total_revenue_quota()-membrane_2.get_total_costs()} €/a")
   print(f"Pressurized Waser Scrubbing balance with quota = {pws.get_total_revenue_quota()-pws.get_total_costs()} €/a")
   print(f"Polyethylene Glycol Scrubbing balance with quota = {pgs.get_total_revenue_quota()-pgs.get_total_costs()} €/a")
   print(f"Pressure Swing Adsorption balance with quota = {psa.get_total_revenue_quota()-psa.get_total_costs()} €/a")
   print(f"Amine Scrubbing balance concessionary taxes = {amine_scrubbing.get_total_revenue_taxes()-amine_scrubbing.get_total_costs()} €/a")
   print(f"Membrane 1 balance concessionary taxes = {membrane_1.get_total_revenue_taxes()-membrane_1.get_total_costs()} €/a")
   print(f"Membrane 2 balance concessionary taxes = {membrane_2.get_total_revenue_taxes()-membrane_2.get_total_costs()} €/a")
   print(f"Pressurized Waser Scrubbing balance concessionary taxes = {pws.get_total_revenue_taxes()-pws.get_total_costs()} €/a")
   print(f"Polyethylene Glycol Scrubbing balance concessionary taxes = {pgs.get_total_revenue_taxes()-pgs.get_total_costs()} €/a")
   print(f"Pressure Swing Adsorption balance concessionary taxes = {psa.get_total_revenue_taxes()-psa.get_total_costs()} €/a")

   # economic steam reforming
   print("\nEconomy Steam Reforming:")
   print(f"Steam Reforming costs = {steam_reforming.get_total_costs()} €/a")
   print(f"Steam Reforming revenue quota = {steam_reforming.get_total_revenue_quota()} €/a")
   print(f"Steam Reforming revenue taxes = {steam_reforming.get_total_revenue_taxes()} €/a")
   print(f"Steam Reforming balance quota = {steam_reforming.get_total_revenue_quota()-steam_reforming.get_total_costs()} €/a")
   print(f"Steam Reforming balance taxes = {steam_reforming.get_total_revenue_taxes()-steam_reforming.get_total_costs()} €/a")

   # economic fischer-tropsch
   print("\nEconomy Fischer-Tropsch Synthesis:")
   print(f"FTS costs = {fischer_tropsch.get_total_costs()} €/a")
   print(f"FTS revenue with quota = {fischer_tropsch.get_total_revenue_with_quota()} €/a")
   print(f"FTS revenue without quota = {fischer_tropsch.get_total_revenue_without_quota()} €/a")
   print(f"FTS balance with quota = {fischer_tropsch.get_total_revenue_with_quota()-fischer_tropsch.get_total_costs()} €/a")
   print(f"FTS balance without quota = {fischer_tropsch.get_total_revenue_without_quota()-fischer_tropsch.get_total_costs()} €/a")


   SQLiteBiogasPlant.conn.commit()
   #SQLiteBiogasPlant.conn.close()
   
   

def makeform(root, fields):
    entries = {}

    # Frame für die erste Spalte
    frame_spalte1 = Frame(root)
    frame_spalte1.grid(row=0, column=0, padx=5, pady=5)

    for i, field in enumerate(fields[:4]):  # Die ersten fünf Felder in der ersten Spalte
        lab = Label(frame_spalte1, width=20, text=field + ": ", anchor='w')
        ent = Entry(frame_spalte1)
        ent.insert(0, "0")
        lab.grid(row=i, column=0, sticky=W, padx=5, pady=5)
        ent.grid(row=i, column=1, sticky=W+E, padx=5, pady=5)
        entries[field] = ent

    # Frame für die zweite Spalte
    frame_spalte2 = Frame(root)
    frame_spalte2.grid(row=0, column=1, padx=5, pady=5)

    for i, field in enumerate(fields[4:]):  # Die letzten beiden Felder in der zweiten Spalte
        lab = Label(frame_spalte2, width=25, text=field + ": ", anchor='w')
        ent = Entry(frame_spalte2)
        ent.insert(0, "0")
        lab.grid(row=i, column=0, sticky=W, padx=5, pady=5)
        ent.grid(row=i, column=1, sticky=W+E, padx=5, pady=5)
        entries[field] = ent

    return entries

# def add_buttons(root, ents, calculate_function1, calculate_function2):
#     # Frame für die Buttons
#     frame_buttons = Frame(root)
#     frame_buttons.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

#     b1 = Button(frame_buttons, text='Ähnliche Anlage finden', command=(lambda e=ents: calculate_function1(e)))
#     b1.pack(side=LEFT, padx=5, pady=5)

#     # Button für die Berechnung der zweiten Spalte
#     b2 = Button(frame_buttons, text='Zweite Spalte berechnen', command=(lambda e=ents: calculate_function2(e)))
#     b2.pack(side=LEFT, padx=5, pady=5)
    
def add_buttons(root, ents, calculate_function1, calculate_function2):
    # Frame für die Buttons
    frame_buttons = Frame(root)
    frame_buttons.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    b1 = Button(frame_buttons, text='Ähnliche Anlage finden', command=(lambda e=ents: calculate_function1(e)))
    b1.pack(side=LEFT, padx=5, pady=5)

    # Button für die Berechnung der zweiten Spalte
    b2 = Button(frame_buttons, text='Jahresbedarf bestimmen', command=(lambda e=ents: calculate_function2(e)))
    b2.pack(side=LEFT, padx=5, pady=5)


   
if __name__ == '__main__':
    root = Tk()
    ents = makeform(root, fields)
    add_buttons(root, ents, final_balance, jahres_bedarf)
    app = ConsoleToGuiApp(root)
    root.mainloop()