import matplotlib.pyplot as plt
import numpy  as np
from math import *
from read_flightradar import read_flightradar
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

a = 6378137
e2 = 0.0066943800229
h_el = 135.4

file = 'W61441_2df0f5fd.csv'
dane = read_flightradar(file)
lotnisko = dane[0, :]
samolot = dane[1:, :]
ft = float(0.3048)

for i in range (len(samolot)):
    samolot[i][9] *= ft
    samolot[i][9] += h_el
    samolot[i][7] = np.deg2rad(samolot[i][7])
    samolot[i][8] = np.deg2rad(samolot[i][8])
    
lotnisko[7] = np.deg2rad(lotnisko[7])
lotnisko[8] = np.deg2rad(lotnisko[8])
lotnisko[9] += h_el

def N(fi):
    return a/np.sqrt(1-e2*np.sin(fi)*np.sin(fi))
def X(N, h, fi, lam):
    return (N+h)*np.cos(fi)*np.cos(lam)
def Y(N, h, fi, lam):
    return (N+h)*np.cos(fi)*np.sin(lam)
def Z(N, h, fi):
    return (N*(1-e2)+h)*np.sin(fi)

L = []
L.append(N(lotnisko[7]))
L.append(X(L[0], lotnisko[9], (lotnisko[7]), (lotnisko[8])))
L.append(Y(L[0], lotnisko[9], (lotnisko[7]), (lotnisko[8])))
L.append(Z(L[0], lotnisko[9], (lotnisko[7])))

Samolot_n = []
S = np.zeros(shape=(len(samolot),3))
for i in range (len(samolot)):
    Samolot_n.append(N(samolot[i,7]))
    S[i][0] = X(Samolot_n[i], samolot[i,9], (samolot[i,7]), (samolot[i,8]))-L[1]
    S[i][1] = Y(Samolot_n[i], samolot[i,9], (samolot[i,7]), (samolot[i,8]))-L[2]
    S[i][2] = Z(Samolot_n[i], samolot[i,9], (samolot[i,7]))-L[3]

R = np.zeros(shape = (3,3))
R[0][0] = -np.sin(lotnisko[7])*np.cos(lotnisko[8])
R[1][0] = -np.sin(lotnisko[7])*np.sin(lotnisko[8])
R[2][0] = np.cos(lotnisko[7])
R[0][1] = -np.sin(lotnisko[8])
R[1][1] = np.cos(lotnisko[8])
R[0][2] = np.cos(lotnisko[7])*np.cos(lotnisko[8])
R[1][2] = np.cos(lotnisko[7])*np.sin(lotnisko[8])
R[2][2] = np.sin(lotnisko[7])

R=R.transpose()
print(R)


x = []
s = []
Az = []
z = []
h = []
for i in range(len(samolot)):
    x.append(R@(S[i,:]))
    s.append(np.sqrt(x[i][0]*x[i][0]+x[i][1]*x[i][1]+x[i][2]*x[i][2]))
    Az.append(np.arctan2(x[i][1],x[i][0]))
    z.append(np.pi/2-np.arcsin(x[i][2]/s[i]))
    h.append(90-np.rad2deg(z[i]))

"""
flh = np.zeros(shape=(len(samolot),2))
for i in range(len(samolot)):
    flh[i][0] = np.rad2deg(samolot[i][7])
    flh[i][1] = np.rad2deg(samolot[i][8])

fig = plt.figure(figsize=(30, 20))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())


# make the map global rather than have it zoom in to
# the extents of any plotted data
extent = [0, 40, 35, 55]
request = cimgt.OSM()
ax = plt.axes(projection=request.crs)
ax.set_extent(extent)
#ax.set_global()
ax.add_image(request, 5)
ax.stock_img()
ax.coastlines()

ax.plot(20.962778, 52.17, 'o', transform=ccrs.PlateCarree())
ax.plot(12.25, 41.79, 'o', transform=ccrs.PlateCarree())
ax.plot([12.25, 20.962778], [41.79, 52.17], transform=ccrs.PlateCarree())
ax.plot([12.25, 20.962778], [41.79, 52.17], transform=ccrs.Geodetic())
ax.plot(flh[:,1], flh[:,0],transform=ccrs.PlateCarree(),color='b')
ax.legend(['Początek trasy - Warszawa', ''])
"""
hours = []
for i in range(len(samolot)):
    hours.append(samolot[i][4])
    hours[i] += (samolot[i][5])/60
    hours[i] += (samolot[i][6])/3600

"""  
fig = plt.figure()
plt.plot(hours, samolot[:,9])
plt.xticks(np.arange(16, 19, 0.50))
plt.yticks(np.arange(0, 14001, 1000.0))
plt.title('Wysokość lotu samolotu w zależności od czasu', fontdict={'fontname': 'Calibri',
                                                 'fontsize': 12})
plt.grid()
plt.xlabel('Godzina', fontdict={'fontname': 'Calibri','fontsize': 12})
plt.ylabel('Wysokość samolotu (m)', fontdict={'fontname': 'Calibri','fontsize': 12})

fig = plt.figure()
plt.plot(hours, samolot[:,10])
plt.xticks(np.arange(16, 19, 0.50))
plt.yticks(np.arange(0, 501, 100.0))
plt.title('Prędkość samolotu w zależności od czasu', fontdict={'fontname': 'Calibri',
                                                 'fontsize': 12})
plt.grid()
plt.xlabel('Godzina', fontdict={'fontname': 'Calibri','fontsize': 12})
plt.ylabel('Prędkość samolotu (km/h)', fontdict={'fontname': 'Calibri','fontsize': 12})

for i in range(len(s)):
    s[i] /=1000
fig = plt.figure()
plt.plot(hours, s)
plt.xticks(np.arange(16, 19, 0.50))
plt.title('Odległość samolotu w zależności od czasu', fontdict={'fontname': 'Calibri',
                                                 'fontsize': 12})
plt.grid()
plt.xlabel('Godzina', fontdict={'fontname': 'Calibri','fontsize': 12})
plt.ylabel('Odległość samolotu (km) ', fontdict={'fontname': 'Calibri','fontsize': 12})

fig = plt.figure()
plt.plot(hours, h)
plt.xticks(np.arange(16, 19, 0.50))
plt.yticks(np.arange(-10, 35, 5))
plt.title('Wysokosć horyzontalna w zależnosci od czasu', fontdict={'fontname': 'Calibri',
                                                 'fontsize': 12})
plt.grid()
plt.xlabel('Godzina', fontdict={'fontname': 'Calibri','fontsize': 12})
plt.ylabel('Wysokosć horyzontalna', fontdict={'fontname': 'Calibri','fontsize': 12})



       
fig = plt.figure()
plt.plot(hours, h)
plt.xticks(np.arange(16, 19, 0.50))
plt.yticks(np.arange(-10, 35, 5))
plt.plot(hours[141], h[0], 'o')
plt.title('Wysokosć horyzontalna w zależnosci od czasu', fontdict={'fontname': 'Calibri',
                                                 'fontsize': 12})
plt.grid()
plt.xlabel('Godzina', fontdict={'fontname': 'Calibri','fontsize': 12})
plt.ylabel('Wysokosć horyzontalna (st)', fontdict={'fontname': 'Calibri','fontsize': 12})
"""       
        
fig = plt.figure(figsize = (10,10))
ax = fig.add_subplot(polar =True)
ax.set_theta_zero_location('N') # ustawienie kierunku północy na górze wykresu
ax.set_theta_direction(-1)
ax.set_yticks(range(0, 90+10, 10))
#Define the yticks
yLabel = ['90', '', '', '60', '', '', '30', '', '', '']
ax.set_yticklabels(yLabel)
ax.set_rlim(0,90)
az_c=[]
s_c=[]
for i in range(len(h)):
    if h[i]>0 and (samolot[i][9])>0:
        az_c.append(Az[i])
        s_c.append(s[i]/1000)
ax.scatter(az_c, s_c, s=6)
ax.plot(hours[141], h[0], 'o')
title = ax.set_title('Wykres Skyplot', fontdict={'fontname': 'Calibri','fontsize': 20})
plt.show()
      
