#This program will quickly generate NARR reanalysis plots for a host of variables with a convenient GUI interface.
#It has been very useful for different case study class projects over the past couple of years, since you can quickly save off the 
#images as they appear.
#It has a few small bugs, such as an inability to loop across different days or years, but I'll get to those eventually.
#My apologies for not having this upgraded to cartopy yet. :)
#Also, sometimes the images and titles get a bit squished when they pop up in the graphics window. If you hit the button to change 
#the layout and select tight layout the problem usually resolves itself.

#Code on github at https://github.com/mwilson14/NARR_GUI


#First, let's set up a GUI using Tkinter
import Tkinter as tk
#Set up the GUI window
top = tk.Tk()
top.title("NARR Map Plotter")
w = tk.Label(top, text = "Let's make some maps! When you're done entering options, click enter and close the window, and maps will eventually appear!")
w.pack(side = tk.LEFT)
#Make the drop-down lists for the year, month, day, and UTC hour
optionlist3 = ('1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016')
optionlist4 = ('01','02','03','04','05','06','07','08','09','10','11','12')
optionlist5 = ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
optionlist6 = ('00','03','06','09','12','15','18','21')
w1 = tk.Label(top, text = "Year")
w1.pack(side = tk.LEFT)
#Associate variables with each of the above lists of options
yearv = tk.StringVar()
yearv.set(optionlist3[0])
monthv = tk.StringVar()
monthv.set(optionlist4[0])
dayv = tk.StringVar()
dayv.set(optionlist5[0])
UTCv = tk.StringVar()
UTCv.set(optionlist6[0])

#Set up the actual drop-down lists in the GUI
mb3 = tk.OptionMenu(top, yearv, *optionlist3)
mb3.pack(side = tk.LEFT)
#e = tk.Entry(top)
#e.pack(side = tk.LEFT)
#month =tk.StringVar()
w2 = tk.Label(top, text = "Month")
w2.pack(side = tk.LEFT)
mb4 = tk.OptionMenu(top, monthv, *optionlist4)
mb4.pack(side = tk.LEFT)
#e1 = tk.Entry(top)
#e1.pack(side = tk.LEFT)
w3 = tk.Label(top, text = "Day")
w3.pack(side = tk.LEFT)
mb5 = tk.OptionMenu(top, dayv, *optionlist5)
mb5.pack(side = tk.LEFT)
#e2 = tk.Entry(top)
#e2.pack(side = tk.LEFT)
w4 = tk.Label(top, text = "UTC Hour")
w4.pack(side = tk.LEFT)
mb6 = tk.OptionMenu(top, UTCv, *optionlist6)
mb6.pack(side = tk.LEFT)
#e3 = tk.Entry(top)
#e3.pack(side = tk.LEFT)

#Make lists of options for the type of event, domain, and number of UTC times requested.
optionlist = ('Severe', 'Winter')
optionlist1 = ('US', 'VUSIT', 'Ohio', 'East Coast')
optionlist2 = ('1', '2')

#Set up the variables with those lists
type = tk.StringVar()
type.set(optionlist[0])
area = tk.StringVar()
area.set(optionlist1[0])
tstep = tk.StringVar()
tstep.set(optionlist2[0])

#Make the actual drop-down lists
mb = tk.OptionMenu(top,type,*optionlist)
mb.pack()
mb1 = tk.OptionMenu(top,area,*optionlist1)
mb1.pack()
mb2 = tk.OptionMenu(top,tstep,*optionlist2)
mb2.pack()

#Set all variables initially to zero
year = 0
month = 0
day = 0
hour = 0

#Launch the actual GUI
def ready():
    global year
    global hour
    global month
    global day
    global UTC
    global event
    global map_area
    global step_s
    #These functions get the variables from the user-selected options in the drop-down list.
    year = yearv.get()
    month = monthv.get()
    month1 = monthv.get()
    day = dayv.get()
    UTC = UTCv.get()
    event = type.get()
    map_area = area.get()
    step_s = tstep.get()
    print(year)
    print(month)
    print(day)
    print(UTC)
    print(event)
    print(map_area)
    print(step_s)
    return year, month, day, UTC, event, map_area, step_s
b = tk.Button(top, text = "Enter", command = ready)
b.pack(side = tk.LEFT)
top.mainloop()

#After GUI is closed, the main program starts.

#Import all the things
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap, cm
from netCDF4 import Dataset
import netCDF4
from netCDF4 import num2date, date2num
import datetime
import math

#These statements were used before the GUI was set up to enter the needed variables
#year, month, day, UTC = raw_input('What time do you need maps for? [Year Month Day UTC]').split()

#Bring in the Severe or Winter event flag to determine which maps to plot/ colormaps to use.
#event = raw_input('Severe or Winter?')

#Ask for additional timesteps
#step_s = raw_input('How many timesteps (3-hourly) (Only works for 1 or 2)?')
step = int(step_s)
#step = stepl + 1

#Ask for map area

#map_area = raw_input('Which area do you want the map for [Ohio, VUSIT, East Coast,or US]?')
#Use these areas to set the map zoom with the npstere definition

#Set level bounds for temperature
if event == 'Severe':
   hi = 115
   lo = 20
   t_int = 2
   colormap = plt.cm.gist_ncar
if event == 'Winter':
   hi = 90
   lo = -40
   t_int = 5
   #colormap = plt.cm.gist_rainbow_r
   #colormap = plt.cm.hsv_r
   #colormap = plt.cm.gist_ncar
   colormap = plt.cm.nipy_spectral
#This converts user input into usable integers
imonth = int(month)
iyear = int(year)
iday = int(day)
iUTC = int(UTC)
syear = str(year)
#byear = iyear*100
#moyear = byear + month1
#smoyear = str(moyear)
smonth = str(month)
sday = str(day)
sUTC = str(UTC)
#Bring in the data drom the openDAP server
temp2=Dataset("http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/monolevel/air.2m."+syear+".nc")
slp = Dataset("http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/monolevel/prmsl."+syear+".nc")
dwp = Dataset("http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/monolevel/dpt.2m."+syear+".nc")
uwn = Dataset("http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/monolevel/uwnd.10m."+syear+".nc")
vwn = Dataset("http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/monolevel/vwnd.10m."+syear+".nc")
capes = Dataset("http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/monolevel/cape."+syear+".nc")
helyeahhelicity = Dataset("http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/monolevel/hlcy."+year+".nc")

#Now let's bring in all of the upper-air stuff!
uptmp = Dataset("http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/pressure/air."+year+smonth+".nc")
hghts = Dataset("http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/pressure/hgt."+syear+smonth+".nc")
upwndu = Dataset("http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/pressure/uwnd."+syear+smonth+".nc")
upwndv = Dataset("http://www.esrl.noaa.gov/psd/thredds/dodsC/Datasets/NARR/pressure/vwnd."+syear+smonth+".nc")

#Bring in the variables from the netCDF file
lats  = temp2.variables['lat'][:]
lons  = temp2.variables['lon'][:]
time = temp2.variables['time']
times = temp2.variables['time'][:]
mtimes = hghts.variables['time'][:]
                                                                                                                                                                                  
n = date2num(datetime.datetime(iyear,imonth,iday,iUTC),time.units)

print(n)

itime = np.where(times == date2num(datetime.datetime(iyear,imonth,iday,iUTC),time.units))
itime2 = np.where(mtimes == date2num(datetime.datetime(iyear,imonth,iday,iUTC),time.units))

print(itime)

print(time[itime])
print(itime2)
print(time[itime2])
#Now let's create the basemap
LLlat = -90
LLlon = 0
URlat = 90
URlon = 360
#Now we create the basemap
Basemap.latlon_default=True

#This definition allows me to select an area of the world to look at on a polar stereographic basemap, which was not easily accomplished with simple Basemap.
#Borrowed from http://code.activestate.com/recipes/578379-plotting-maps-with-polar-stereographic-projection-/

def polar_stere(lon_w, lon_e, lat_s, lat_n, **kwargs):
   '''Returns a Basemap object (NPS/SPS) focused in a region.
   lon_w, lon_e, lat_s, lat_n -- Graphic limits in geographical coordinates.
   W and S directions are negative.
   **kwargs -- Aditional arguments for Basemap object.

   '''
   lon_0 = lon_w + (lon_e - lon_w) / 2.
   ref = lat_s if abs(lat_s) > abs(lat_n) else lat_n
   lat_0 = math.copysign(90., ref)
   proj = 'npstere' if lat_0 > 0 else 'spstere'
   prj = Basemap(projection=proj, lon_0=lon_0, lat_0=lat_0,
                          boundinglat=0, resolution='c')
   #prj = pyproj.Proj(proj='stere', lon_0=lon_0, lat_0=lat_0)
   lons = [lon_w, lon_e, lon_w, lon_e, lon_0, lon_0]
   lats = [lat_s, lat_s, lat_n, lat_n, lat_s, lat_n]
   x, y = prj(lons, lats)
   ll_lon, ll_lat = prj(min(x), min(y), inverse=True)
   ur_lon, ur_lat = prj(max(x), max(y), inverse=True)
   return Basemap(projection='stere', lat_0=lat_0, lon_0=lon_0,
                           llcrnrlon=ll_lon, llcrnrlat=ll_lat,
                           urcrnrlon=ur_lon, urcrnrlat=ur_lat, **kwargs)

#Use the definition to plot the basemap
#If you want to change the area plotted, change these coordinates.
#Ohio Zoom
if map_area == 'Ohio':

   m = polar_stere(-95, -71, 35, 50, resolution ='l')
   #set separation for wind barbs
   brb = 2
#Full US Zoom
if map_area == 'US':

   m = polar_stere(-120, -72, 25, 50.5, resolution ='l')
   brb = 5
#Zoom for chaseable domain of the Valpo Storm Intercept Team
if map_area == 'VUSIT':

   m = polar_stere(-105, -81, 35, 50, resolution ='l')
   #set separation for wind barbs
   brb = 2
#East Coast Snowstorm Zoom
if map_area == 'East Coast':

   m = polar_stere(-95, -64, 25, 48, resolution ='l')
#set separation for wind barbs
   brb = 3

#add more map areas later


#Make a loop to run multiple timesteps
#For some reason, this loop only works with one or two timesteps, but for the purposes I've used this for that's all that's really needed.
a = 1
for i in range(step):

   #Start bringing in the actual atmospheric data
   #Bring in only the data from the time we need.
   #first we have temperature
   airk = temp2.variables['air'][itime]
   airf = (airk-273.15)*(9.0/5.0)+32
   print np.shape(airf)
   #Now we'll bring in pressure
   mslp = slp.variables['prmsl'][itime]
   msl = mslp/100
   #Now we'll bring in dewpoint
   dew = dwp.variables['dpt'][itime]
   dewf = (dew-273.15)*(9.0/5.0)+32
   #Now we'll bring in the winds and convert them to kts
   u = uwn.variables['uwnd'][itime]
   v = vwn.variables['vwnd'][itime]
   uwnks = u*1.944
   vwnks = v*1.944
   #Now we'll start plotting some maps. 
   #Set up our plot and draw in the map
   plt.style.use('bmh')
   plt.figure(a,figsize=(30,24))
   m.drawcoastlines(linewidth=0.5)
   m.drawcountries(linewidth=0.5) # Draw country boundaries
   #Draw some lats and lons
   m.drawstates(linewidth=0.5)
   m.drawparallels(np.arange(-90.,90.,10),labels=[1,0,0,0])
   m.drawmeridians(np.arange(0.,360.,10),labels=[0,0,0,1])
   #Create levels to plot temps, using the bounds from Severe or Winter
   levels = np.arange(lo,hi,t_int)
   #lonsg,latsg = np.meshgrid(lons, lats)
   #Plot the temperatures with a color fill. This may need to change for the cold season
   csc = m.contourf(lons,lats,airf[0,:,:],levels,cmap=colormap,latlon=True)
   plt.colorbar(csc,orientation='vertical', shrink = .5)
   #Now let's plot the pressures
   plevels = np.arange(928,1060,4)
   cs = m.contour(lons,lats,msl[0,:,:],plevels,linewide=1.0,colors='k',latlon=True)
   plt.clabel(cs, fontsize=10, inline=1, inline_spacing=18, fmt='%i', rightside_up=True)
   #Now let's plot the dewpoints
   dlevels = np.arange(50,85,5)
   cs1 = m.contour(lons,lats,dewf[0,:,:],dlevels,linewide=1.0,colors='g',latlon=True)
   plt.clabel(cs1, fontsize=10, inline=1, inline_spacing=18, fmt='%i', rightside_up=True)
   #Finally, we'll plot some wind barbs
   windb = m.barbs(lons[1::brb,1::brb],lats[1::brb,1::brb],uwnks[0,1::brb,1::brb],vwnks[0,1::brb,1::brb],barbcolor='k',length = 5.5,latlon = True)
   plt.title('NARR Surface Map',loc='left')
   #plt.title(datetime.datetime(iyear,imonth,iday,iUTC), loc = 'right')
   vtime = num2date(time[itime],time.units)
   plt.title(vtime[0], loc = 'right')


   #Now let's make some upper-level maps.
   #Let's bring in all of the upper-air data
   #Bring in the height values.
   hgt = hghts.variables['hgt'][itime2]
#Bring in the temps!
   uairk = uptmp['air'][itime2]
   uairc = uairk - 273.15
   #Bring in the capes!
   cape = capes.variables['cape'][itime]
   #and Helicity
   hel = helyeahhelicity.variables['hlcy'][itime]
   #and the winds
   uu = upwndu.variables['uwnd'][itime2]
   vu = upwndv.variables['vwnd'][itime2]
   upwnd = (((vu)**2+(uu)**2)**(.5))*1.944
   uwnk = uu*1.944
   vwnk = vu*1.944

   #Let's set up a second figure
   #Next task: Make a for loop to go through all of the different levels for a particular time.
   #Create an if statement for the contour levels,
   #setting the appropriate contours for each level.
   a = a + 1
   for l in [6,16,20]:
      plt.figure(a,figsize=(30,24))
      plt.style.use('bmh')
      m.drawcoastlines(linewidth=0.5)
      m.drawcountries(linewidth=0.5) # Draw country boundaries
      #Draw some lats and lons
      m.drawstates(linewidth=0.5)
      m.drawparallels(np.arange(-90.,90.,10),labels=[1,0,0,0])
      m.drawmeridians(np.arange(0.,360.,10),labels=[0,0,0,1])
      #Create height levels and plot the heights
      if l == 6:
         hlevels = np.arange(1050,1620,30)
         Clevels = np.arange(-50,50,5)
         uwlevels = np.arange(20,100,5)
         title = 'NARR 850mb Height, Temp, and Wind'
      elif l == 16:
         hlevels = np.arange(4980,6000,60)
         Clevels = np.arange(-80,20,5)
         uwlevels = np.arange(30,200,20)
         title = 'NARR 500mb Height, Temp, and Wind'
      elif l == 20:
         hlevels = np.arange(8640,9960,120)
         Clevels = np.arange(-90,20,5)
         uwlevels = np.arange(50,200,20)
         title = 'NARR 300mb Height, Temp, and Wind'

      cs2 = m.contour(lons,lats,hgt[0,l,:,:],hlevels,linewide=1.0,colors='k',latlon=True)
      plt.clabel(cs2, fontsize=10, inline=1, inline_spacing=18, fmt='%i', rightside_up=True)
      cs3 = m.contour(lons,lats,uairc[0,l,:,:],Clevels,linewide=1.0,linestyles = '--',colors='r',latlon=True)
      plt.clabel(cs3, fontsize=10, inline=1, inline_spacing=18, fmt='%i', rightside_up=True)
      csc1 = m.contourf(lons,lats,upwnd[0,l,:,:],uwlevels,cmap=plt.cm.cool,latlon=True)
      plt.colorbar(csc1,orientation='vertical', shrink = .5)
      cf1 = m.contour(lons,lats,upwnd[0,l,:,:],uwlevels,linewide=0.1,linestyles='dashed',colors='b',latlon=True)
      windb = m.barbs(lons[1::2*brb,1::2*brb],lats[1::2*brb,1::2*brb],uwnk[0,l,1::2*brb,1::2*brb],vwnk[0,l,1::2*brb,1::2*brb],barbcolor='k',length = 6,latlon = True)
      plt.clabel(cf1, fontsize=10, inline=1, inline_spacing=18, fmt='%i', rightside_up=True, colors ='k')
      plt.title(title, loc = 'left')
      #plt.title(datetime.datetime(iyear,imonth,iday,iUTC), loc = 'right')
      vtime = num2date(time[itime],time.units)
      plt.title(vtime[0], loc = 'right')
      a = a+1
      
      if l == 16:
        #vort = metcalc.kinematics.v_vorticity(uu[0,l,:,:],vu[0,l,:,:],32500,32500)
        #print np.shape(uu)
        #print np.shape(vu)
        dx = np.array(np.gradient(uu[0,l,:,:]))
        dy = np.array(np.gradient(vu[0,l,:,:]))
        #eventually, I'll calculate vorticity the correct way by accounting for the variable lat/lon grid spacing, but this at least provides a good idea of where stuff is.
        vort = ((dy/32500)-(dx/32500))*100000
        print(vort)
        plt.figure(a,figsize=(30,24))
        plt.style.use('bmh')
        m.drawcoastlines(linewidth=0.5)
        m.drawcountries(linewidth=0.5) # Draw country boundaries
        #Draw some lats and lons
        m.drawstates(linewidth=0.5)
        m.drawparallels(np.arange(-90.,90.,10),labels=[1,0,0,0])
        m.drawmeridians(np.arange(0.,360.,10),labels=[0,0,0,1])
        vorlevels = np.arange(-20,28,1)
        cs2 = m.contour(lons,lats,hgt[0,l,:,:],hlevels,linewide=1.0,colors='k',latlon=True)
        plt.clabel(cs2, fontsize=13, inline=1, inline_spacing=30, fmt='%i', rightside_up=True)
        cf2 = m.contourf(lons, lats, vort[0,:,:], vorlevels, cmap = plt.cm.hsv_r, latlon= True)
        plt.colorbar(cf2,orientation='vertical', shrink = .5)
        plt.title('500 mb Height and Vorticity', loc = 'left')
        vtime = num2date(time[itime],time.units)
        plt.title(vtime[0], loc = 'right')
        a = a+1

   #Use an if statement to only make these maps for severe weather events.
   if event == 'Severe':

      a = a+1
      #Now we'll plot some maps of shear and CAPE!
#Starting with Sfc-850mb
      plt.figure(a,figsize=(30,24))
      plt.style.use('bmh')
      m.drawcoastlines(linewidth=0.5)
      m.drawcountries(linewidth=0.5) # Draw country boundaries
      #Draw some lats and lons
      m.drawstates(linewidth=0.5)
      m.drawparallels(np.arange(-90.,90.,10),labels=[1,0,0,0])
      m.drawmeridians(np.arange(0.,360.,10),labels=[0,0,0,1])
      #Set up levels for CAPE!
      capelevels = np.arange(500,8000,500)
      cs3 = m.contour(lons,lats,cape[0,:,:],capelevels,linewide=1.0,colors='r',latlon=True)
      plt.clabel(cs3, fontsize=10, inline=1, inline_spacing=10, fmt='%i', rightside_up=True, colors ='r')
      #Plot surface pressure
      cs4 = m.contour(lons,lats,msl[0,:,:],plevels,linewide=1.0,colors='k',latlon=True)
      #plt.clabel(cs4, fontsize=10, inline=1, inline_spacing=.8, fmt='%i', rightside_up=True)
      #Now let's calculate the shear-850mb shear
      ushr8 = uwnk[0,6,:,:]-uwnks[0,:,:]
      vshr8 = vwnk[0,6,:,:]-vwnks[0,:,:]
      shear8 = (((vshr8)**2+(ushr8)**2)**(.5))
      shrlevels = np.arange(10,60,5)
      cscs = m.contourf(lons,lats,shear8,shrlevels,cmap=plt.cm.gist_earth,latlon=True)
      shrb = m.barbs(lons[1::2*brb,1::2*brb],lats[1::2*brb,1::2*brb],ushr8[1::2*brb,1::2*brb],vshr8[1::2*brb,1::2*brb],barbcolor='b',length = 6,latlon = True)
      plt.colorbar(cscs,orientation='vertical', shrink = .5)
      plt.title('NARR CAPE and SFC-850mb Shear (kts)', loc = 'left')
      plt.title(vtime[0], loc = 'right')
      #Now let's plot the sfc-500mb shear
      a = a+1

      plt.figure(a,figsize=(30,24))
      plt.style.use('bmh')
      m.drawcoastlines(linewidth=0.5)
      m.drawcountries(linewidth=0.5) # Draw country boundaries
      #Draw some lats and lons
      m.drawstates(linewidth=0.5)
      m.drawparallels(np.arange(-90.,90.,10),labels=[1,0,0,0])
      m.drawmeridians(np.arange(0.,360.,10),labels=[0,0,0,1])
      #Plot the cape and mslp
      capelevels = np.arange(500,8000,500)
      cs8 = m.contour(lons,lats,cape[0,:,:],capelevels,linewide=1.0,colors='r',latlon=True)
      plt.clabel(cs8, fontsize=10, inline=1, inline_spacing=18, fmt='%i', rightside_up=True, colors ='r')
      #Plot surface pressure
      cs9 = m.contour(lons,lats,msl[0,:,:],plevels,linewide=1.0,colors='k',latlon=True)
     # plt.clabel(cs9, fontsize=10, inline=1, inline_spacing=.8, fmt='%i', rightside_up=True)
      plt.clabel(cs9, fontsize=10, inline=1, inline_spacing=18, fmt='%i', rightside_up=True)

      #Calculate and plot the sfc-500 and sfc-850 shear
      ushr5 = uwnk[0,16,:,:]-uwnks[0,:,:]
      vshr5 = vwnk[0,16,:,:]-vwnks[0,:,:]
      shear5 = (((vshr5)**2+(ushr5)**2)**(.5))
      shrlevels5 = np.arange(35,90,5)
      cscs = m.contourf(lons,lats,shear5,shrlevels5,cmap=plt.cm.gist_earth,latlon=True)
      shrb5 = m.barbs(lons[1::2*brb,1::2*brb],lats[1::2*brb,1::2*brb],ushr5[1::2*brb,1::2*brb],vshr5[1::2*brb,1::2*brb],barbcolor='b',length = 6,latlon = True)
      plt.colorbar(cscs,orientation='vertical', shrink = .5)
      plt.title('NARR CAPE and SFC-500mb Shear (kts)', loc = 'left')
      #plt.title(datetime.datetime(iyear,imonth,iday,iUTC), loc = 'right')
      vtime = num2date(time[itime],time.units)
      plt.title(vtime[0], loc = 'right')
      a = a+1
      
      #Now plot a helicity map
      plt.figure(a,figsize=(30,24))
      plt.style.use('bmh')
      m.drawcoastlines(linewidth=0.5)
      m.drawcountries(linewidth=0.5) # Draw country boundaries
      #Draw some lats and lons
      m.drawstates(linewidth=0.5)
      m.drawparallels(np.arange(-90.,90.,10),labels=[1,0,0,0])
      m.drawmeridians(np.arange(0.,360.,10),labels=[0,0,0,1])
      #Define levels for everything, with separate levels for the fill and contour of helicity to make it look a bit better
      helllevels = np.arange(100,800,50)
      helllevels7 = np.arange(100,2000,50)
      capelevels = np.arange(500,8000,500)
      cs3 = m.contour(lons,lats,cape[0,:,:],capelevels,linewide=1.0,colors='r',latlon=True)
      plt.clabel(cs3, fontsize=13, inline=1, inline_spacing=18, fmt='%i', rightside_up=True, colors ='r')
      cs5 = m.contour(lons,lats,hel[0,:,:],helllevels7,linewide=1.0,colors='b',latlon=True)
      plt.clabel(cs5, fontsize=13, inline=1, inline_spacing=18, fmt='%i', rightside_up=True, colors ='b')
      chel = m.contourf(lons,lats,hel[0,:,:],helllevels,cmap=plt.cm.Blues,extend = 'max',latlon=True)
      plt.colorbar(chel,orientation='vertical', shrink = .5)
      #Plot surface pressure
      cs6 = m.contour(lons,lats,msl[0,:,:],plevels,linewide=1.0,colors='k',latlon=True)
      plt.clabel(cs6, fontsize=13, inline=1, inline_spacing=18, fmt='%i', rightside_up=True)
      windb = m.barbs(lons[1::2*brb,1::2*brb],lats[1::2*brb,1::2*brb],uwnks[0,1::2*brb,1::2*brb],vwnks[0,1::2*brb,1::2*brb],barbcolor='r',length = 6,latlon = True)
      windub = m.barbs(lons[1::2*brb,1::2*brb],lats[1::2*brb,1::2*brb],uwnk[0,16,1::2*brb,1::2*brb],vwnk[0,16,1::2*brb,1::2*brb],barbcolor='b',length = 6,latlon = True)
      plt.title('NARR CAPE, SFC-3 km Helicity, and SFC-500mb Crossover', loc = 'left')
      vtime = num2date(time[itime],time.units)
      plt.title(vtime[0], loc = 'right')
      a = a+1
      
      #Calculate Supercell Composite from (slightly modified to account for sfc-500 shear instead of sfc-6km) definition on SPC mesoanalysis page
      sup_comp = np.zeros((277,349))
      for i in range(277):
        for j in range(349):
            if shear5[i,j] > 38.8769:
                sup_comp[i,j] = (cape[0,i,j]/1000)*(hel[0,i,j]/50)*(1)
            elif shear5[i,j] < 19.4384:
                sup_comp[i,j] = (cape[0,i,j]/1000)*(hel[0,i,j]/50)*(0)
            else:
                sup_comp[i,j] = (cape[0,i,j]/1000)*(hel[0,i,j]/50)*(shear5[i,j]/38.8769)
      plt.figure(a,figsize=(30,24))
      plt.style.use('bmh')
      m.drawcoastlines(linewidth=0.5)
      m.drawcountries(linewidth=0.5) # Draw country boundaries
      #Draw some lats and lons
      m.drawstates(linewidth=0.5)
      m.drawparallels(np.arange(-90.,90.,10),labels=[1,0,0,0])
      m.drawmeridians(np.arange(0.,360.,10),labels=[0,0,0,1])
      #Define levels for supercell composite
      complevels = [1,2,4,8,12,16,20,24,28,32,36,40,44,48,52]
      capelevels = np.arange(500,8000,500)
      #cs3 = m.contour(lons,lats,cape[0,:,:],capelevels,linewide=1.0,colors='r',latlon=True)
      #plt.clabel(cs3, fontsize=13, inline=1, inline_spacing=.8, fmt='%i', rightside_up=True, colors ='r')
      cs5 = m.contour(lons,lats,sup_comp,complevels,linewide=1.0,colors='b',latlon=True)
      plt.clabel(cs5, fontsize=13, inline=1, inline_spacing=18, fmt='%i', rightside_up=True, colors ='b')
      chel = m.contourf(lons,lats,sup_comp,complevels,cmap=plt.cm.Blues,latlon=True)
      plt.colorbar(chel,orientation='vertical', shrink = .5)
      #Plot surface pressure
      cs6 = m.contour(lons,lats,msl[0,:,:],plevels,linewide=1.0,colors='k',latlon=True)
      plt.clabel(cs6, fontsize=13, inline=1, inline_spacing=18, fmt='%i', rightside_up=True)
      windb = m.barbs(lons[1::2*brb,1::2*brb],lats[1::2*brb,1::2*brb],uwnks[0,1::2*brb,1::2*brb],vwnks[0,1::2*brb,1::2*brb],barbcolor='r',length = 6,latlon = True)
      windub = m.barbs(lons[1::2*brb,1::2*brb],lats[1::2*brb,1::2*brb],uwnk[0,16,1::2*brb,1::2*brb],vwnk[0,16,1::2*brb,1::2*brb],barbcolor='b',length = 6,latlon = True)
      plt.title('NARR Supercell Composite and SFC-500mb Crossover', loc = 'left')
      vtime = num2date(time[itime],time.units)
      plt.title(vtime[0], loc = 'right')
      a = a+1


   itime = itime[0] + 1
   itime2 = itime2[0] + 1

plt.show()
                                                                                                                                                                          
