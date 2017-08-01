from netCDF4 import Dataset
import numpy
import os.path
#hardcoded origin to save time
runtime ="18z"
iorg = 743
jorg = 1640
gridspacing = 3 #km
t=0
while 1:
    ncfile ="../data/nam.t"+runtime+".conusnest.hiresf%02d.tm00.nc" % t
    if not os.path.isfile(ncfile):
        break
    print ncfile
    root = Dataset(ncfile,'r')
    vars = root.variables
    
    u = 3.6*numpy.squeeze(vars["UGRD_10maboveground"][:,:,:]) #m/s 2 km/h
    v = 3.6*numpy.squeeze(vars["VGRD_10maboveground"][:,:,:])
    udesired = u[(iorg-158):(iorg+159),(jorg-158):(jorg+159)]
    vdesired = v[(iorg-158):(iorg+159),(jorg-158):(jorg+159)]
    dim =  udesired.shape
    print dim
    
    f = open('roms%04d.dat' % t, 'w')
    f.write("Surface Velocity ROMS data (km/hr)\n")	
    f.write("Domain Center 41.3209371228N, 289.46309961W\n")
    f.write("#Data_XMin = "+str(-1*(dim[1]-1)/2*gridspacing)+"\n")
    f.write("#Data_XMax = "+str((dim[1]-1)/2*gridspacing)+"\n")
    f.write("#Data_XRes = "+str(dim[1])+"\n")
    f.write("#Data_YMin = "+str(-1*(dim[0]-1)/2*gridspacing)+"\n")
    f.write("#Data_YMax = "+str((dim[0]-1)/2*gridspacing)+"\n")
    f.write("#Data_YRes = "+str(dim[0])+"\n")
    f.write("ZONE T=\"%04d\" I=" % (t+1) +str(dim[1])+" J="+str(dim[0])+"\n")
    for i in range(dim[0]):
        for j in range(dim[1]):
            f.write(str(udesired[i,j])+" "+str(vdesired[i,j])+"\n")

    f.close()
    
    t+=1
       


