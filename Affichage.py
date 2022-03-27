from Classes import *
import matplotlib.pyplot as pb

path='/Users/bellrancurel/Desktop/Jo_mesures_son/'
dossier='data'
data=Dossier(path+dossier)
freq, mag, phase=data.calcul()

pb.figure()
pb.plot(freq, phase, label='Phase')
pb.plot(freq, mag, label='Magnitude')
pb.xscale('log')
pb.title('Resultat')
pb.savefig('resultat.png')
pb.show()
