# Title: bg_process_modelv13.py
# About this version 13: Weakness of the code has been discussed and agreed upon with VMCallo and DBGamez
from BGgeothermal3 import *
import pandas as pd
from t2thermo_rnc import *
import math

def Enthliq(p):
    '''Enter pressure in MPag'''
    hf, hg = Enthalpy(p*1e6)
    return hf

def Enthgas(p):
    '''Enter pressure in MPag'''
    hf, hg = Enthalpy(p*1e6)
    return hg

def sep_steam_frac(twophaseenthalpy, separatorpressure):
    '''Separator pressure is in Pascal and enthalpy in J/kg'''
    return separated_steam_fraction(twophaseenthalpy, separatorpressure)


file = "bom_v13.xls"
owhp = pd.read_excel(file, sheetname = "Well OperatingPressure")
ws = pd.read_excel(file, sheetname = "BOM EQUATION coeffs", parse_cols="A,H:T")
ws2 = pd.read_excel(file, sheetname = "Vessel Info")
ws3 = pd.read_excel(file, sheetname = "ChemistryData")

svlist = {}
svwell = {}
data = {}
finalinfo = {}
chemlist = {}
sv_out = {}

for eachindex in range(len(ws.index)):

    wellname = ws.iloc[eachindex,0]
    mf1, mf2, mf3, mf4, mf5, mf6, h1, h2, h3, h4, h5, sep_press, vessel = map(lambda x: ws.iloc[eachindex, x],range(1, 14))

    well_headpressure = owhp.iloc[eachindex,1]

    welldata = WellClass(well_headpressure, mf1, mf2, mf3, mf4, mf5, mf6, h1, h2, h3, h4, h5)#, sep_press, vessel)

    data[wellname] = [welldata.massflow(),welldata.enthalpy()]

    if vessel not in svwell.keys():
        svwell[vessel] = [wellname]
    else:
        templist = svwell[vessel]
        templist.append(wellname)
        svwell[vessel] = templist

for i in range(len(ws2.index)):
    svlist[ws2.iloc[i, 0]] = [ws2.iloc[i, 1],ws2.iloc[i, 2]]

for i in range(len(ws3.index)):
    # the format chemlist["PAL12D"] = [Cl,SiO2, CO2, H2S]"
    chemlist[ws3.iloc[i,0]] = [ws3.iloc[i,1],ws3.iloc[i,2],ws3.iloc[i,3],ws3.iloc[i,4]]

mixing_lines = [['sv3034','sv3056','sv3012'],['sv4034','sv4012','sv4050'],['sv5080'],['sv7000']]

for each_mixingline in mixing_lines:
    totalMx = 0
    totalMxHx = 0
    wellCO2 = 0
    wellH2S = 0
    wellSiO2 = 0

    for eachline in each_mixingline:
        welllist = svwell[eachline]
        #print(eachline,welllist)
        for eachwell in welllist:
            well_mf = data[eachwell][0]
            well_enth = data[eachwell][1]

    for eachvessel in each_mixingline:
        # remember that this loop calculates the total mass flow and average enthalpy of a specific vessel
        welllist = svwell[eachvessel]
        totalTPmf = 0
        totalTPenth = 0
        p = svlist[eachvessel][0]

        for eachwell in welllist:
            TPmassflow = data[eachwell][0]
            TPenthalpy = data[eachwell][1]
            totalTPenth += TPmassflow*TPenthalpy*1e3
            totalTPmf += TPmassflow
            wellCO2 += TPmassflow * chemlist[eachwell][2]
            wellH2S += TPmassflow * chemlist[eachwell][3]
            wellSiO2 += TPmassflow * chemlist[eachwell][1]

        mx = totalTPmf # MASS FLOW coming from a set of wells in a "vessel"
        Hx = (totalTPenth/mx) # average enthalpy coming from a set of wells
        totalMx += mx # mass flow of the entire mixing line composed of 3 vessels
        totalMxHx += (mx*Hx)

    aveSiO2 = wellSiO2 / totalMx
    aveCO2 = wellCO2/totalMx
    aveH2S = wellH2S/totalMx

    # Note: This is a weakness of the code as it assumes the separator pressure is the same for the 3 vessels. As per discussion with VMCallos, this is ok.
    Hfg = Enthgas(p)-Enthliq(p) #
    mg = (totalMxHx-(totalMx*Enthliq(p)))/Hfg
    mf = totalMx - mg

    for eachvessel in each_mixingline:
        ms_outvessel = svlist[eachvessel][1]*mg #.36*mg
        mb_outvessel = svlist[eachvessel][1]*mf
        CO2_outvessel = aveCO2 #CO2_outvessel = aveCO2*svlist[eachvessel][1]
        H2S_outvessel = aveH2S #H2S_outvessel = aveH2S*svlist[eachvessel][1]
        SiO2_outvessel = aveSiO2 #SiO2_outvessel = aveSiO2*svlist[eachvessel][1]
        svp = svlist[eachvessel][0]
        #print 'MG',mg
        #print("eachvessel", "totalMx", "mg", "mf", "ms_outvessel", "CO2_outvessel", "H2S_outvessel", SiO2_outvessel)
        #print(eachvessel, svp, totalMx, mg, mf, ms_outvessel, mb_outvessel,CO2_outvessel,H2S_outvessel,SiO2_outvessel)
        sv_out[eachvessel] = [svp, ms_outvessel, mb_outvessel, CO2_outvessel, H2S_outvessel, SiO2_outvessel]
        x = ms_outvessel/(ms_outvessel+mb_outvessel)
        print(svp, ms_outvessel, mb_outvessel,x , CO2_outvessel/x, H2S_outvessel/x, SiO2_outvessel, SiO2_outvessel/(1-x))
        
        
#print svlist
