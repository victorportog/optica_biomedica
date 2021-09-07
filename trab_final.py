import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pymcx as mcx

mcx_local = r'C:\Program Files\MCXStudio\MCXSuite\mcxcl\bin\mcxcl.exe'

cfg = mcx.create()

#print(cfg.items())
#print(cfg.keys())

cfg['Session']['Photons'] = 1E7 #setting number of photons
cfg['Session']['ID'] = 'trab_final' #setting simulation id
cfg['Shapes'][0]['Grid']['Size'] = [100, 100, 100] #setting simulation size
cfg['Optode']['Source']['Pos'] = [50, 50, 0] #setting position of the source  
cfg['Domain']['LengthUnit'] = 1E-2 #setting that each voxel has a 10^-2 mm length 
cfg['Domain']['Media'].pop()

# three layers (air, epidermis, dermis)
cfg['Shapes'].append({'ZLayers': [[1,10,1], [11,15,2], [16,100,3]]})
cfg['Domain']['Media'].append({'mua':0, 'mus':0, 'g':0, 'n':1})
cfg['Domain']['Media'].append({'mua':23.054, 'mus':9.39, 'g':0.9, 'n':1.37})
cfg['Domain']['Media'].append({'mua':0.045, 'mus':35.65, 'g':0.9, 'n':1.37})

# blood vessel
cfg['Shapes'].append({'Cylinder':{'Tag':4, 'C0':[50,0,50], 'C1':[50,100,50], 'R':10}})
cfg['Domain']['Media'].append({'mua':1.657E1, 'mus':37.59, 'g':0.9, 'n':1.37})

print(cfg)

data_mch, data_mc2 = mcx.run(cfg=cfg, flag='--repeat 3', mcxbin=mcx_local)
#print(data_mc2.shape)

#plotting the fluence 2D map (slicing at y=50)
plt.figure()
cmap = mpl.cm.jet
plt.imshow(np.squeeze(np.log10(data_mc2[:,50,:])).T, cmap=cmap)
plt.xlabel('x [10$^{-2}$mm]')
plt.ylabel('z [10$^{-2}$mm]')
plt.colorbar(cmap=cmap, orientation='vertical', label='log(Fluence Rate [1/mm$^2$s])')

plt.figure()
z_range = np.arange(10,100,1)
plt.plot(np.squeeze(np.log10(data_mc2[50,50,:])), '.', color='g')
plt.vlines(10,6.5,12.5)
plt.vlines(15,6.5,12.5)
plt.vlines(40,6.5,12.5)
plt.vlines(50,6.5,12.5, linestyles='dashed')
plt.vlines(60,6.5,12.5)
plt.axis([0,100,6.5,12.5])
plt.xlabel('z [10$^{-2}$mm]')
plt.ylabel('log(Fluence Rate [1/mm$^2$s])')

plt.show()