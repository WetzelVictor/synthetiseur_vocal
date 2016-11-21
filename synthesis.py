# -*- coding: utf-8 -*-
# File synthesis.py
"""
Projet: Vocal controlled synthL
date: octobre 2016
UPMC, Master SdI, acoustique
@authors: lauraparra & victorwetzel
"""


import numpy as np

class oscillator:
    """ class oscillator:
    Cette classe permet de générer une forme d'onde. 
    Il faut tout d'abord créer un vecteur temps, dont la longueur est définie 
    par la fréquence fondamentale f0 (create_time).
    La méthode 'create_wave' permet de modifier la variable de champs 'wave' en fonction
    de f0.
    """
    def __init__(self, f0=440., AMP=0.5, ampSine=0.5, ampSaw=0.5, ampTriangle=0.5,SAMPLERATE=44100):
        
        self.AMP = AMP
        
        self.ampSine = ampSine
        self.ampSaw = ampSaw
        self.ampTriangle = ampTriangle

        self.SAMPLERATE = SAMPLERATE       
        self.SAMPLELENGTH = 1. / float(SAMPLERATE)

        self.f0 = float(f0)
        self.T0 = 1./float(f0)
        
        self.time = np.linspace(0,self.T0,self.T0/self.SAMPLELENGTH)

        self.wave = np.zeros(int(self.T0/self.SAMPLELENGTH))
        self.SINE = self.wave
        self.SAW = self.wave
        self.TRIANGLE = self.wave 


    def sine(self):
        """ sine(): Permet de générer une onde sinusoïdale en fonction
        des attributs de la classe"""
        SINE = self.ampSine * np.sin(2.*np.pi*self.f0*self.time)
        return SINE

    def triangle(self):
        """ triangle(): Permet de générer une onde triangle en fonction
        des attributs de la classe"""
        TRIANGLE = self.ampTriangle * 2./np.pi * np.arcsin(np.sin(2.*np.pi*self.f0*self.time))
        return TRIANGLE

    def saw(self):
        """ triangle(): Permet de générer une onde en dents de scie en fonction
        des attributs de la classe"""      
        w0 = 2.*np.pi*self.f0
        SAW = self.ampSaw * (np.arctan(np.tan(w0*self.time/2.)))/np.pi
        return SAW

    def create_time(self):
        """ create_time(): Génère un vecteur temps en fonction des attributs de
        la classe"""
        self.time = np.linspace(0,1/self.f0,float(self.SAMPLERATE)/self.f0)


    def create_wave(self):
        """ create_wave(): Met à jour la forme d'onde 'wave'. """
        self.create_time()
        self.wave = self.AMP*(self.sine() + \
                    self.triangle() + \
                    self.saw()   )

