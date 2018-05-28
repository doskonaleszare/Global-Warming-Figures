# -*- coding: utf-8 -*-
"""
author: Femke Nijsse

Shared under Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)

You are free to:
Share — copy and redistribute the material in any medium or format
Adapt — remix, transform, and build upon the material
for any purpose, even commercially. 

Under the following terms:
Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original. 
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np

from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import matplotlib as mpl
mpl.rcParams['font.size'] = 15

language_version='English'
if language_version=='English':
    ice_age = 'Ice age \n cycles'
    indust= 'Industrial revolution starts'
    co2con = 'CO$_2$ concentration (ppmv)'
    thyrago = 'Thousands of years ago'
    year = 'year (CE)'
    
if language_version=='Dutch':
    ice_age = 'IJstijdcycli'
    indust= 'Begin industriële revolutie'
    co2con = 'CO$_2$ concentratie (ppmv)'
    thyrago = 'Duizenden jaar geleden'
    year = 'jaar (CE)'
    
    


"""
Import CO2 composite data from Bereiter et al
"""

url = 'https://www1.ncdc.noaa.gov/pub/data/paleo/icecore/antarctica/antarctica2015co2composite.txt'
df = pd.read_csv(url, skiprows=138, sep="\t", header=None)

# 	-51-1800 yr BP: Law Dome (Rubino et al., 2013)
#	1.8-2 kyr BP:	Law Dome (MacFarling Meure et al., 2006)
#	2-11 kyr BP:	Dome C (Monnin et al., 2001 + 2004)
#	11-22 kyr BP:	WAIS (Marcott et al., 2014) minus 4 ppmv (see text)
#	22-40 kyr BP:	Siple Dome (Ahn et al., 2014)
#	40-60 kyr BP:	TALDICE (Bereiter et al., 2012)
#	60-115 kyr BP:	EDML (Bereiter et al., 2012)
#	105-155 kyr BP:	Dome C Sublimation (Schneider et al., 2013)
#	155-393 kyr BP:	Vostok (Petit et al., 1999)
#	393-611 kyr BP:	Dome C (Siegenthaler et al., 2005)
#	612-800 kyr BP:	Dome C (Bereiter et al., 2014)
#

df.columns = ['yr', 'CO2', 'unc']

df_lawdome_all = df[df.yr <= 2000]
df_domeC1 = df[(df.yr > 2000) & (df.yr <= 11000)]
df_wais = df[(df.yr > 11000) & (df.yr <= 22000)]
df_siple = df[(df.yr > 22000) & (df.yr <= 40000)]
df_taldice = df[(df.yr > 40000) & (df.yr <= 60000)]
df_edml = df[(df.yr > 60000) & (df.yr <= 115000)]
df_domeC2 = df[(df.yr > 105000) & (df.yr <= 155000)]
df_Vostok = df[(df.yr > 155000) & (df.yr <= 393000)]
df_domeC3 = df[df.yr > 393000]

df_last1k = df[df.yr <= 950]

"""
Import Mauna Loa data
"""

df_mlo = pd.read_csv('monthly_in_situ_co2_mlo.csv',skiprows=54)
df_mlo=df_mlo[['  Yr','CO2filled']]
df_mlo.columns = ['yr', 'CO2']
df_mlo = df_mlo[df_mlo.yr != '1958']
df_mlo = df_mlo[df_mlo.yr != '2018']
df_mlo = df_mlo.drop([0,1])

#Take yearly averages
yeararray = np.arange(1959,2018)
co2matrix = np.zeros((len(yeararray),2))
for n in yeararray:
    jan_yr_n = 12*(n-1959)
    dec_yr_n = 12*(n-1959)+12
    mon = df_mlo.iloc[jan_yr_n:dec_yr_n,1]
    meanmon = np.mean([float(item) for item in mon])        
    co2matrix[n-1959]=np.array([n,meanmon])
    


"""
Make the plot
"""

#Initialise
fig,ax = plt.subplots()

#Add data
ax.plot((1950-co2matrix[:,0])/1000,co2matrix[:,1],'k',linewidth=1.5)
ax.plot(df_lawdome_all['yr']/1000,df_lawdome_all['CO2'],'C2',linewidth=2)
ax.plot(df_domeC1['yr']/1000,df_domeC1['CO2'],'C1',linewidth=1)
ax.plot(df_wais['yr']/1000,df_wais['CO2'],'C3',linewidth=1)
ax.plot(df_siple['yr']/1000,df_siple['CO2'],'C4',linewidth=1)
ax.plot(df_taldice['yr']/1000,df_taldice['CO2'],'C5',linewidth=1)
ax.plot(df_edml['yr']/1000,df_edml['CO2'],'C6',linewidth=1)
ax.plot(df_domeC2['yr']/1000,df_domeC2['CO2'], 'C9',linewidth=1)
ax.plot(df_Vostok['yr']/1000,df_Vostok['CO2'],'C0',linewidth=1)
ax.plot(df_domeC3['yr']/1000,df_domeC3['CO2'], 'C9',linewidth=1)

#Add box for inset
xy_box_low = (0.933,0.45)
width_box,height_box = 0.03,0.53
xy_box_high = (xy_box_low[0],xy_box_low[1]+height_box)
xy_inset_low = (0.89,0.735)
xy_inset_high = (0.89,0.915)

ax.add_patch(
    patches.Rectangle(
        xy_box_low,   # (x,y)
        width_box,          # width
        height_box,          # height
        fill=False,
        alpha=0.8,
        transform=ax.transAxes,
        linewidth=0.8
    )
)
    

ax.annotate("", xy=xy_box_low, xytext=xy_inset_low,
             arrowprops=dict(arrowstyle="-",alpha=0.9,linewidth=0.8),
             xycoords='axes fraction')
ax.annotate("", xy=xy_box_high, xytext=xy_inset_high,
             arrowprops=dict(arrowstyle="-",alpha=0.9,linewidth=0.8),
             xycoords='axes fraction')



#Mark-up
ax.set_xlabel(thyrago)
ax.set_ylabel(co2con)
ax.invert_xaxis()
ax.yaxis.tick_right()
ax.yaxis.set_label_position("right")
ax.set_facecolor('xkcd:pale peach')


#Inset figure
axins = inset_axes(ax, 3.95,0.7, bbox_to_anchor=(384, 290))
axins.plot(1950-df_last1k['yr'],df_last1k['CO2'],'C2',linewidth=2.2)
axins.plot(co2matrix[:,0],co2matrix[:,1],'k',linewidth=2.2)


axins.set_xlabel(year,fontsize=13,labelpad=-0.2)
axins.tick_params(labelsize=13,direction='in')

# sub region of the original image
x1, x2, y1, y2 = 1000, 2025, 260,420
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)

# fix the number of ticks on the inset axes
axins.yaxis.get_major_locator().set_params(nbins=4)
axins.xaxis.get_major_locator().set_params(nbins=5)


ax.text(0.15,0.37,ice_age, size=12, ha="center", 
         transform=ax.transAxes)
#axins.text(0.15 ,0.8, indust,\
#           size=12, ha="left", transform=ax.transAxes)
axins.annotate(indust, xy=(1750, 295), xytext=(1200, 370),
            arrowprops=dict(facecolor='black', alpha=0.7, arrowstyle='->'),fontsize=12,
            )


plt.draw()
plt.savefig('test2.svg', bbox_inches='tight')



