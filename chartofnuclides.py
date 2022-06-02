# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 15:15:47 2021

@author: isaia
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By

path = "C:\\Users\\isaia\\Documents\\"

timedict = {
	"GeV": 3.291e-25,
	"MeV": 3.291e-22,
	"keV": 3.291e-19,
	"eV": 3.291e-16,
	"fs": 1e-15,
	"ps": 1e-12,
	"ns": 1e-9,
	"μs": 1e-6,
	"ms": 1e-3,
	"s": 1,
	"m": 60,
	"h": 3600,
	"d": 86400,
	"y": 31536000
	}

elementals = [
	"H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni",\
	"Cu","Zn", "Ga","Ge", "As","Se", "Br","Kr", "Rb","Sr", "Y","Zr", "Nb","Mo", "Tc","Ru", "Rh","Pd", "Ag","Cd", "In","Sn", "Sb","Te", "I","Xe", "Cs","Ba", "La","Ce",\
	"Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po",\
	"At","Rn","Fr","Ra","Ac","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds",\
	"Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og"
	]

def open_nndc(nucleus):
	driver = webdriver.Edge("C:\edgedriver_win32\msedgedriver.exe")
	driver.get("https://www.nndc.bnl.gov/nudat2/getdatasetClassic.jsp?nucleus={}&unc=nds".format(nucleus))
	elements = driver.find_elements(By.TAG_NAME, "p")
	elem = driver.find_elements(By.TAG_NAME, "a")
	
	i=0
	for e in elem:
		i+=1
		if e.text == "      0.0" or e.text == "  0":
			print(e.text)
			final=i+3
			break
	
	j=0
	for index in [4,3,2]:
		if index == 2:
			okay = elements[2].find_elements(By.TAG_NAME, "tr")
			deeper = okay[1].find_elements(By.TAG_NAME, "td")
			for k in deeper:
				j+=1
				print(deeper[j-1].text)
				if float(deeper[j-1].text) == 0:
					print(j)
					break

	# 		print(deeper[2].text)

			halflife = 10000000000000000000000000000000000000000
			if deeper[j+1].text == "STABLE":
				print(nucleus, end="\t")
				print(halflife)
			else:
				str_halflife = deeper[j+1].text.split("\n")[0]
				halflife = float(str_halflife.split()[0])*timedict[str_halflife.split()[1]]
				print(nucleus, end="\t")
				print(halflife) # try to do units of seconds
		
			driver.close()
			break
		try:
			okay = elements[index].find_elements(By.TAG_NAME, "tr") #6H needs to elements[3] probably but deeper[j+1]
	# 		print(okay[0].text)
			deeper = okay[1].find_elements(By.TAG_NAME, "td")
			
			for k in deeper:
				j+=1
				if float(deeper[j-1].text) == 0:
	# 				print(j)
					break
	
	#
	# 		print(deeper[0].text)
			
			halflife = 10000000000000000000000000000000000000000
			if deeper[j+2].text == "STABLE":
				print(nucleus, end="\t")
				print(halflife)
			else:
				try:
					str_halflife = deeper[j+2].text.split("\n")[0]
					halflife = float(str_halflife.split()[0])*timedict[str_halflife.split()[1]]
					print(nucleus, end="\t")
					print(halflife) # try to do units of seconds
				except ValueError:
					halflife = 0
					print(nucleus, end="\t")
					print(halflife) # try to do units of seconds

			driver.close()
			break
		except IndexError:
			continue


class nuclei:

	def __init__(self,path):
		nuclei.filepath = path+'NuclearHalfLives.csv'

	def load_array(self):
		self.nucleus = [[1],[0],[10000000000000000000000000000000000000000],["1H"]]
		with open(self.filepath,"r") as self.file:
			next(self.file)
			for line in self.file:
				Z = int(line.split(",")[0])
				A = int(line.split(",")[1])
				N = A-Z
				T = float(line.split(",")[2])
				nuclide = "{}{}".format(A,elementals[Z-1])
				try:
					if Z == self.nucleus[0][-1] and N == self.nucleus[1][-1]:
						continue
					else:
						self.nucleus[0].append(Z)
						self.nucleus[1].append(N)
						self.nucleus[2].append(T)
						self.nucleus[3].append(nuclide)
				except IndexError:
					continue


chart = nuclei(path)
chart.load_array()
# open_nndc("6H")
for i in [3,4,5,6]:
 	open_nndc(chart.nucleus[3][i])

# =============================================================================
# print(chart.nucleus[0][-1])
# print(chart.nucleus[1][-1])
# 
# fig, ax = plt.subplots(tight_layout=True)
# fig.gca().set_ylabel(r'$Z$')
# fig.gca().set_xlabel(r'$N$')
# 
# Z_number = [i for i in range(len(chart.nucleus[0]))]
# number_34z_y = [18 for i in range(17)]
# number_34z_x = [i for i in range(17)]
# number_34n_x = [16 for i in range(19)]
# number_34n_y = [i for i in range(19)]
# 
# hist = ax.hist2d(chart.nucleus[1], chart.nucleus[0],bins=(int(chart.nucleus[1][-1]),int(chart.nucleus[0][-1])), norm=mpl.colors.LogNorm(), weights = chart.nucleus[2],  cmap=mpl.cm.jet)
# nz_line = plt.plot(Z_number,Z_number,color="red")
# z34Ar = plt.plot(number_34z_x,number_34z_y,color="gray",linewidth=2.0)
# n34Ar = plt.plot(number_34n_x,number_34n_y,color="gray",linewidth=2.0)
# 
# cbar = fig.colorbar(hist[3], ax=ax)
# cbar.set_label(r'Half Life   [s]', rotation = 270, size=11)
# 
# plt.rcParams.update({'font.size': 13})
# fig.set_size_inches(10, 5)
# fig.savefig('C:\\Users\\isaia\\Pictures\\nuclidic_chart_ty_fatima.png', dpi=300)
# 
# fig, ax = plt.subplots(tight_layout=True)
# 
# #weighto=[1,0.022027948,0.00359222,0.02726862,0.666667,1,0.043020783,0.496396693,14.6,16.56757541,1,7.609686734,0.53,0.127491395,0.018005925,1]
# weighto=[1,0.813292847,0.414388583,0.049630838,\
# 0.04,1,0.134415794,0.024470589,\
# 0.5,5.302576795,1,0.120063315,\
# 1.3,0.127491395,1.141226609,1]
# 
# #heatmap = [[0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3],[3,2,1,0,3,2,1,0,3,2,1,0,3,2,1,0],[1,0.022027948,0.00359222,0.02726862,0.666667,1,0.043020783,0.496396693,14.6,16.56757541,1,7.609686734,0.53,0.127491395,0.018005925,1]]
# #heatmap = [[3,3,3,3,2,2,2,2,1,1,1,1,0,0,0,0],[0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3],[weighto[-i] for i in range(len(weighto))]]
# heatmap = [[3,3,3,3,2,2,2,2,1,1,1,1,0,0,0,0],[0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3],weighto]
# 
# hist = ax.hist2d(heatmap[1], heatmap[0],bins=range(5),norm=mpl.colors.LogNorm(), weights = heatmap[2],  cmap=mpl.cm.jet)
# 
# # for i in range(4):
# #     for j in range(4):
# #         ax.text(j+0.5,i+0.5,heatmap[2][4*(3-i)+j],
# #                 color="w", ha="center", va="center", fontweight="bold")
# ax.set_aspect('equal')
# 
# cbar = fig.colorbar(hist[3], ax=ax)
# cbar.set_label(r'C [arb.]', rotation = 270)
# 
# plt.rcParams.update({'font.size': 14})
# fig.set_size_inches(10, 10)
# fig.savefig('C:\\Users\\isaia\\Pictures\\contaminated_nuclidic_heatmap.png', dpi=150)
# =============================================================================
