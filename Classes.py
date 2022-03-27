#Classes descriptives du dossier et fichiers son
from os import listdir
import numpy as np

class Dossier():
    def __init__(self, folder):
        """
16 fichiers txt dans chaque dossier
        :param folder: folder absolute name
        """

        self.folder = folder
        self.name = folder_name(self.folder)
        self.files = files_list(folder)

    def calcul(self):
        big_freq=self.files[0].frequency
        big_mag=[]
        big_phase=[]
        for i in self.files:
            truc=i.calcul_fichier()
            big_phase += [truc[0]]
            big_mag+= [truc[1]]
        final_phase=np.array(big_phase)
        final_mag=np.array(big_mag)
        max_phase=final_phase.max(axis=0)
        max_mag=final_mag.max(axis=0)

        text='Frequency\t Magnitude max\t Phase max\n'
        for ind in range(0, 720):
            text+=str(big_freq[ind])+'\t'+str(max_mag[ind])+'\t'+str(max_phase[ind])+'\n'
        Result=open(self.folder+'_results.txt', 'w')
        Result.write(text)
        return (big_freq, max_mag, max_phase)

class Fichier():
    def __init__(self, file, Hz):
        """

        :param file: Absolute name of a file
        """
        text=file_reader(file)
        self.file = file
        self.name = file_name(file)
        self.text=text
        self.hz=Hz
        self.frequency=self.text[0]
        self.magnitude=self.text[1]
        self.phase=self.text[2]

    def calcul_fichier(self):
        result=petit_calcul(self.frequency, self.magnitude, self.phase, self.hz)
        return result

#Fonctions pour alleger le code des classes
def folder_name(folder):
    """

    :param folder: str, folder name (absolute)
    :return: name (only last folder)
    """
    i = -1
    while folder[i] != '/':
        i += -1
    return folder[i+1:]

def file_name(file):
    """

    :param file: str, file name
    :return: name without extension
    """
    i = -1
    while file[i] != '/':
        i += -1
    return file[i+1:-4]

def file_reader(nom):
    file=open(nom)
    text=file.readlines()
    frequency=[]
    magnitude=[]
    phase=[]
    for ligne in text[5:]:
        ind=ligne.index('\t')
        freq, rest=ligne[:ind], ligne[ind+1:]
        ind = ligne.index('\t')
        mag, rest = rest[:ind], rest[ind+1:-1]
        frequency+=[float(freq)]
        magnitude+=[float(mag)]
        phase+=[float(rest)]
    frequency=np.array(frequency)
    magnitude=np.array(magnitude)
    phase=np.array(phase)
    return (frequency, magnitude, phase)

def files_list(folder):
    """
    Help for the settings of Folder class
    :param folder:
    :return:
    """
    fichier = listdir(folder)
    fichier.sort()
    result=[]
    ind=0
    Hz=[320, 250, 200, 160, 125, 100, 80, 63, 50, 40, 32, 25, 20, 16, 12.5, 10]
    for i in fichier[1:]:
        result+=[Fichier(folder+'/'+i, Hz[ind])]
        ind+=1
    return result

def petit_calcul(freq, mag, phase, min):
    tour = 0
    liste_tour=[]
    fenetre=[]
    reponsedB=[]
    for i in range(0, 720):
        if freq[i]<min:
            fenetre+=[0]
            reponsedB+=[0]
        else:
            if phase[i] > 0 and phase[i - 1] < 0:
                tour += 1
                liste_tour+=[tour]
            fenetre+=[phase[i]-(tour*360)]
            reponsedB+=[mag[i]]
    return (fenetre, reponsedB)
