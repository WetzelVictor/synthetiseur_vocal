# -*- coding: utf-8 -*-
# File main.py
"""
Projet: Vocal controlled synthL
date: octobre 2016
UPMC, Master SdI, acoustique
@authors: lauraparra & victorwetzel
"""

""" === LIBRAIRIES === """
# Import des différentes librairies
import numpy as np
import pylab as plt
import analyse # Nathan Whitehead
import pyaudio 
import threading
import logging
import time

# Classes
import get_sample as get
import synthesis as syn
import SVconsole as csl

# Fichier de debugging, permettant notamment de 
# traquer les opérations dans les différents threads.
# Il suffit d'ajouter la ligne de commande:  logging.debug('<commentaire>')
# à l'endroit désiré 
logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )




""" ==== CONSTANTES === """
MONO = 1
SAMPLE_RATE = 44100
FORMAT = pyaudio.paInt16
BUFFER_SIZE = 512

prev_pitch  = 440
prev_volume = 0

PITCH_THRESHOLD = 4




""" === INSTANCIATION ===
	- Instanciation des différents objets:
		1-) Serveur et Flux audio (entrant et sortant)
		2-) Oscillateur
		3-) Console
"""

# === Serveur et Flux Audio ===
# Permet de lire ou d'écrire sur le flux audio
audioPort = pyaudio.PyAudio()

stream = audioPort.open(
            	format = FORMAT,
            	channels = MONO,
            	rate = SAMPLE_RATE,
            	input = True,
            	output = True)


# === Oscillateur ===
# Permet de créer une forme d'onde spécifique.
# Trois ondes différentes sont ajoutées: sinus, triangle et dents de scie
OSC = syn.oscillator(f0 = 20., AMP=0., ampSine=1., ampTriangle=0., ampSaw = 0.)
prev_pitch = 0


# === Console ===
# Permet de démarrer et d'arrêter le programme.
console = csl.Console()





""" ================================== """
""" === FONCTIONS CONCURRENTIELLES === 
	On distingue trois threads différents, c'est à dire trois sous-programmes
	qui s'éxécutent en même temps:
		1-) 'branchAnalyze()' qui se charge d'analyser le flux audio entrant.
		Elle subdivisée en deux sous-fonctions:
		
			a°) analyseChunk(): réalise deux opérations d'analyse. D'une part
			le volume de la trame "CHUNK", et la fréquence fondamentale d'autre part.
			Une structure conditionnelle permet de passer outre certaines
			erreurs de détection de la hauteur.
			SI la fonction "detect_pitch" retourne None
			ALORS la hauteur est la hauteur précédente.

			b°) OSCdriver(): Modifie les variables de champs de l'oscillateur.
			Met à jour le vecteur temps et le vecteur de forme d'onde de 
			l'oscillateur

		2-) 'branchProduce()' qui se charge d'écrire en continu la forme d'onde.
			sur le flux audio.

		3-) 'branchConsole()' dont la variable de champs <stop> est
			la condition d'exécution des structures while dans les autres threads.
"""

def analyseChunk(CHUNK):
	""" analyseChunk(CHUNK):

	Cette fonction détermine le volume et la hauteur de la trame CHUNK.

	INPUT  = Trame d'échantillions (np.array)
	OUTPUT = list(volume,pitch)

	See Nathan Whitehead's GitHub for further details on the <analyse> module.
	"https://github.com/ExCiteS/SLMPi/tree/master/SoundAnalyse-0.1.1"
	 """
	global prev_pitch 
	volume = analyse.loudness(CHUNK) # Calcul du Volume

	pitch  = analyse.detect_pitch(CHUNK) # Calcul de la hauteur
	if pitch == None:		# Structure conditionnelle de fin
		pitch = prev_pitch
	else: 
		prev_pitch = pitch

	return [volume, pitch]

def OSCdriver(param):
	""" OSCdriver(param):
	
	Cette fonction permet de modifier les variables de champs 'f0' et 
	'AMP' d'un objet de type 'oscillateur' (module: synthesis).
	Met à jour le vecteur temps et la forme d'onde.

	INPUT  = liste[volume, hauteur]
	OUTPUT = None

	Voir <synthesis.py> pour plus de de détails.
	"""
	OSC.AMP = param[0]
	
	if param[1] == 0:
		param[1] = 1

	
	OSC.f0  = param[1]

	#OSC.create_time() # Met à jour le vecteur temps nécessaire à...
	OSC.create_wave() # ... la création de la forme d'onde.
	return


def branchAnalyze():
	"""branchAnalyze():
	Contient toutes les opérations d'analyse.
	 """
	while(not console.stop):
		CHUNK = get.record(stream,1024) # Acquisition des échantillions
		OSCdriver(analyseChunk(CHUNK))  # Analyse des échantillons. Mise à jour des 
										# attributs de l'objet 'OSC' généré par la
										# classe oscillateur. 
	logging.debug('Exiting')
	return

def branchProduce():
	while(not console.stop):
		if(OSC.AMP <= 0.):
			None
		else:
			stream.write(np.ndarray.tostring(np.float16(OSC.wave)))
	logging.debug('Exiting')
	return

def branchConsole():
	"""branchConsole():
	Permet à l'utilisateur d'arrêter le programme à l'aide de la commande "stop".
	"""
	console.ask()
	logging.debug('Exiting')


""" ================================ """
""" === ANTICHAMBRE DE LA BOUCLE === """
# Cette section instancie les objets threads des trois fonctions
# <branch> définit ci-dessus.

threadConsole = threading.Thread(name = 'CONSOLE',
								 target = branchConsole)

threadAnalyze = threading.Thread(name='ANALYZE',
								 target = branchAnalyze)

threadProduce = threading.Thread(name='PRODUCE', 
								 target = branchProduce)

""" === BOUCLE IMPLICITE PRINCIPALE === """
""" La boucle 'while' est contenue dans les différents threads.
	La condition d'éxécution de ces boucles est contrôlée
	par l'object <console>.
"""

# Demande à l'utilisateur si il veut démarrer le programme.
console.askFirst()

# Quand l'utilisateur entre 'y' pour démarrer le programme,
# Les trois threads sont démarrés: <thread.start()>.
threadConsole.start()
threadAnalyze.start()
threadProduce.start()



""" === TERMINATING ==="""


# Quand l'utilisateur entre la commande 'stop', les trois threads
# arrêtent de s'éxécuter.

# la commande <thread.join()> demande au programme principal d'attendre
# que les threads soient fini afin de continuer.
threadProduce.join()
threadAnalyze.join()
threadConsole.join()

# Fermeture du flux audio
stream.stop_stream()
stream.close()
audioPort.terminate()



""" 				========================
					=== Fin du programme ===
 					========================
"""