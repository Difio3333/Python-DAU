import random as rd
import time
import pygame,sys
from PIL import Image
import threading
import copy
import pyaudio
import wave
import mido
import chords

pygame.init()


class Piano():

	def __init__(self):
		self.chordlist = ["create_major","create_5th","create_suspended_4th","create_suspended_2nd","create_added_9th","create_major_6th","create_6th_added_9th","create_major_7th","create_major_9th","create_major_7th_sharp_11th","create_major_13th","create_minor","create_minor_added_9th","create_minor_6th","create_minor_flat_6th","create_minor_6th_added_9th","create_minor_7th","create_minor_7th_flat_5th","create_minor_9th","create_minor_11th","create_minor_13th","create_dominant_7th","create_7th_suspended_4th","create_9th","create_9th_suspended_4th","create_11th","create_13th","create_13th_suspended_fourth","create_augmented_7th","create_minor_major_7th","create_diminished","create_diminished_7th_chord","create_half_diminished_7th_chord"]
		self.chordDict = {}
		self.keydict = {}
		self.rhythmOne = [0.4,0.4,0.4,0.4]
		self.rhythmTwo = [0.4,0.4,0.4,0.4]
		self.recording = False
		self.time = 0
		self.record = []
		self.screenCount = 0
		self.set_up_piano()
		self.midiInstrument = self.setup_midi_keyboard()
		self.blues = False
		self.chord_recording = False
		self.recorded_chords = []
		self.autochordCheck = False

		self.key = "C Major"
		self.keyNumber = 0
		self.register = 12
		
		self.progressions = self.return_all_chord_progessions()
		self.progression = self.progressions[0]
		self.repetitions = 0
		self.chordstep = 0
		self.songKey = None
		self.songProgression = None

		self.deltatime = 0
		self.solotime = 0
		self.loops = 0
		self.midiNote = None

	def setup_midi_keyboard(self):
		instruments = mido.get_input_names()
		port = None

		for entry in instruments:
			print(entry)
			#Change "Vortes Wireless 2" to the name of your Midi Keyboard.
			#also check line 76 for further setup.
			if entry == "Vortex Wireless 2":
				port = entry 
				break
		port = mido.open_input(port)
			
		return port

	def listen_midi(self):
		if self.midiInstrument:
			for msg in self.midiInstrument.iter_pending():
				if msg.type == "note_on":
					self.midiNote = msg.note
					
				else:
					pass
					
	def play_midi(self):
		if self.midiNote:
			#You may need to change the -47 here to something that fits to your keyboard. 1 is equal to one semitone step.
			self.play_chord([self.midiNote-47])
			self.midiNote = None
	
	def record_wav_audio(self):
		if self.autochordCheck == False:
			self.autochordCheck = True
			import autochord
		self.chord_recording = True
		self.recorded_chords = []
		audio = pyaudio.PyAudio()
		info = audio.get_host_api_info_by_index(0)
		numdevices = info.get('deviceCount')
		inputdevice = 0
		for i in range(0, numdevices):
			if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
				print("Check line 95 of the code. Here you have to manually input your own Recording device.")
				print("Input Device id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
				#change BLUE NESSIE USB MIC to the name of your microphone!
				if audio.get_device_info_by_host_api_device_index(0, i).get('name') == "BLUE NESSIE USB MIC":
					inputdevice = i
					break
				
		stream = audio.open(format=pyaudio.paInt16,channels=2,rate=44100,input=True,frames_per_buffer=1024,input_device_index=inputdevice)

		frames=[]

		
		print("Recording")
		while True:
			data = stream.read(1024)
			frames.append(data)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_x:
						self.chord_recording = False
			if self.chord_recording == False:
				break
		
		stream.stop_stream()
		stream.close()
		audio.terminate()

		sound_file = wave.open("myrecording.wav","wb")

		sound_file.setnchannels(2)
		sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
		sound_file.setframerate(44100)
		sound_file.writeframes(b''.join(frames))
		sound_file.close()
		record_chords = autochord.recognize('myrecording.wav', lab_fn='chords.lab')
		for chord in record_chords:
			if chord[2] == "N":
				pass
			else:
				self.recorded_chords.append(chord[2])
		self.recorded_chords = list(dict.fromkeys(self.recorded_chords))

	def convert_recorded_chords(self):
		pass

	def create_major(self,note):
		firstNote = note	
		secondNote = note+4
		thirdNote = note+7
		
		return [firstNote,secondNote,thirdNote]

	def create_minor(self,note):
		firstNote = note	
		secondNote = note+3
		thirdNote = note+7
		
		return [firstNote,secondNote,thirdNote]
	
	def create_diminished(self,note):
		firstNote = note
		secondNote = note+3
		thirdNote = note+6
		return [firstNote,secondNote,thirdNote]

	def transcribe_notes(self,chord):
		
		transcribed_chord = []
		if type(chord) == int:
			note = chord
			tone = self.transcribe_basic_tone(note)
			if tone:
				tone = tone.lower()			
			if note > 0 and note <= 9:
				transcribed_chord.append(tone+"3")
			elif note >= 10 and note <= 21:
				transcribed_chord.append(tone+"4")
			elif note >= 22 and note < 31:
				transcribed_chord.append(tone+"5")
			else:
				pass
		
		else:
			i = 0
			for note in chord:
				if type(note) == int:
					tone = self.transcribe_basic_tone(note)
					if tone:
						tone = tone.lower()
					
					if note > 0 and note <= 9:
						transcribed_chord.append(tone+"3")
					elif note >= 10 and note <= 21:
						transcribed_chord.append(tone+"4")
					elif note >= 22 and note < 31:
						transcribed_chord.append(tone+"5")
					else:
						pass

					i+=1
			
		return transcribed_chord

	def transcribe_guitar_notes(self,chord):
		transcribed_chord = []
		i = 0
		for note in chord:
			if type(note) == int:
				tone = self.transcribe_basic_tone(note)
				if note > 0 and note <= 9:
					transcribed_chord.append(tone)
				elif note >= 10 and note < 21:
					transcribed_chord.append(tone)
				elif note >= 22 and note < 31:
					transcribed_chord.append(tone)
				else:
					pass

				i+=1
		return transcribed_chord

	def transcribe_basic_tone(self,note):
		transcribed_basic_tone = None

		if note % 12 == 1:
			transcribed_basic_tone = "C"
		elif note % 12 == 2:
			transcribed_basic_tone = "C-"
		elif note % 12 == 3:
			transcribed_basic_tone = "D"
		elif note % 12 == 4:
			transcribed_basic_tone = "D-"
		elif note % 12 == 5:
			transcribed_basic_tone = "E"
		elif note % 12 == 6:
			transcribed_basic_tone = "F"
		elif note % 12 == 7:
			transcribed_basic_tone = "F-"
		elif note % 12 == 8:
			transcribed_basic_tone = "G"
		elif note % 12 == 9:
			transcribed_basic_tone = "G-"
		elif note % 12 == 10:
			transcribed_basic_tone = "A"
		elif note % 12 == 11:
			transcribed_basic_tone = "A-"
		elif note % 12 == 0:
			transcribed_basic_tone = "B"
		else:
			pass
		return transcribed_basic_tone

	def create_major_scale(self,note):
		note -= 24
		
		scale=[]
		
		majorscale = [2,2,1,2,2,2,1]
		i = 0
		while i < 5:
			z = 0
			while z < len(majorscale):
				note += majorscale[z]
				scale.append(note)
				z+=1
			i+=1
		
		return scale

	def create_dorian_scale(self,note):
		note -= 24
		
		scale=[]
		
		majorscale = [2,1,2,2,2,1,2]
		i = 0
		while i < 5:
			z = 0
			while z < len(majorscale):
				note += majorscale[z]
				scale.append(note)
				z+=1
			i+=1
		
		return scale

	def create_phrygian_scale(self,note):
		note -= 24
		
		scale=[]
		
		majorscale = [1,2,2,2,1,2,2]
		i = 0
		while i < 5:
			z = 0
			while z < len(majorscale):
				note += majorscale[z]
				scale.append(note)
				z+=1
			i+=1
		
		return scale

	def create_major_pentatonic_scale(self,note):
		
		scale=[]
		
		majorPentatonicScale = [2,2,3,2,3]
		
		i = 0
		while i < 1:
			z = 0
			while z < len(majorPentatonicScale):
				note += majorPentatonicScale[z]
				scale.append(note)
				z+=1
			i+=1
		return scale

	def create_major_blues_scale(self,note):
		
		scale=[]
								 
		majorPentatonicScale = [3,2,1,1,3,2]
		
		i = 0
		while i < 1:
			z = 0
			while z < len(majorPentatonicScale):
				note += majorPentatonicScale[z]
				scale.append(note)
				z+=1
			i+=1
		return scale

	def create_minor_pentatonic_scale(self,note):
		
		scale=[]
								 
		minorPentatonicScale =  [3,2,2,3,2]
								 

		z = 0
		while z < len(minorPentatonicScale):
			note += minorPentatonicScale[z]
			scale.append(note)
			z+=1
		
		return scale

	def create_dorian_pentatonic_scale(self,note):
		
		scale=[]
								 
		dorianPentatonicScale =  [3,2,2,2,1,2]
							 
		z = 0
		while z < len(dorianPentatonicScale):
			note += dorianPentatonicScale[z]
			scale.append(note)
			z+=1
		
		return scale

	def create_minor_blues_scale(self,note):
		
		scale=[]
								 
		minorPentatonicScale =  [3,2,1,1,3,2]
								 
		i = 0
		while i < 1:
			z = 0
			while z < len(minorPentatonicScale):
				note += minorPentatonicScale[z]
				scale.append(note)
				z+=1
			i+=1
		return scale

	def create_minor_scale(self,note):
		note -= 24
		scale = []
		minorscale = [2,1,2,2,1,2,2]
		i = 0
		while i < 4:
			z = 0
			while z < len(minorscale):
				note += minorscale[z]
				scale.append(note)
				z+=1
			i+=1 
		
		return scale

	def create_persian_scale(self,note):
		note -= 24
		scale = []
		persianscale = [1,3,1,1,2,3,1]
		persianscale = [1,3,1,2,2,1,3]
		#persianscale = [1,3,1,2,2,1,2]

		i = 0
		while i < 5:
			z = 0
			while z < len(persianscale):
				note += persianscale[z]
				scale.append(note)
				z+=1
			i+=1 
		
		return scale

	def create_all_keys(self):
		all_keys = []
		
		note = 1
		while note < 13:
			all_keys.append([self.transcribe_basic_tone(note) + " Major"] + self.create_major_scale(note))
			all_keys.append([self.transcribe_basic_tone(note) + " Minor"] + self.create_minor_scale(note))
			all_keys.append([self.transcribe_basic_tone(note) + " Dorian"] + self.create_dorian_scale(note))
			#all_keys.append([self.transcribe_basic_tone(note) + " Persian"] + self.create_persian_scale(note))
			
			note+=1
		
		note = 1
		while note < 13:
			self.keydict[self.transcribe_basic_tone(note) + " Major"] = self.create_major_scale(note)			
			self.keydict[self.transcribe_basic_tone(note) + " Minor"] = self.create_minor_scale(note)
			self.keydict[self.transcribe_basic_tone(note) + " P-Major"] = self.create_major_pentatonic_scale(note)
			self.keydict[self.transcribe_basic_tone(note) + " PB-Major"] = self.create_major_blues_scale(note)
			self.keydict[self.transcribe_basic_tone(note) + " P-Minor"] = self.create_minor_pentatonic_scale(note)
			self.keydict[self.transcribe_basic_tone(note) + " PB-Minor"] = self.create_minor_blues_scale(note)
			self.keydict[self.transcribe_basic_tone(note) + " P-Major"] = self.create_major_pentatonic_scale(note)
			self.keydict[self.transcribe_basic_tone(note) + " Dorian"] = self.create_dorian_pentatonic_scale(note)
			note += 1
		
		return all_keys

	def check_if_chord_in_key(self,key,chord):
		chord = tuple(chord)
		
		for note in chord:
			if type(note) == str:
				pass 
			elif note not in key:
				return
			else:
				pass
		if key[0] in self.chordDict:
			self.chordDict[key[0]] += [chord]
		else:
			self.chordDict[key[0]] = [chord]
			
	def play_chord_progression_from_key(self,key):
		progression = self.create_chord_progression_CIRCLE_TWO()

		a = 0

		while a < 50:
			
			deltatime = time.time()
			
			i = 0
			e = 0
			while True:
				
				if i % len(progression) == 0:
					e+=1
					e = e%len(progression)
				self.play_chord(self.chordDict[key][progression[e]],volume = 0.2)
							
			
				if time.time() - deltatime >= 0.8:
					tone = rd.randint(1, 5) 
					self.play_chord([self.keydict[self.find_pentatonic(key)][tone-1]+12])
					deltatime = time.time()
				time.sleep(0.4)
				i+=1

			a+=1
	
	def play_solo(self,key,tempo):
		progression = self.create_chord_progression_CIRCLE_TWO()
		
		a = 0

		while a < 50:
			
			i = 0

			while i < len(progression):
				e=0
				deltatime = time.time()
				
				while e < 4:					

					if time.time() - deltatime >= 0.2:
						tone = rd.randint(1, 3)						
						self.play_chord([self.chordDict[key][progression[i]][tone]+12],volume=0.4,instrument="Piano")
					time.sleep(tempo)
				i+=1
									
			a+=1

	def convert_chord_names(self,chord):
		
		chordName = ""
		
		if chord.endswith("-m"):
			chordName = chord[0] + "- Minor"
		elif chord[-1] == "m":
			chordName = chord[0] + " Minor"
		elif chord[-1] == "-":
			chordName = chord[0] + "- Major"
		elif len(chord) == 1:
			chordName = chord[0] + " Major"
		else:
			chordName = chord[0] + "°"
	
		return chordName

	def find_pentatonic(self,key):
		pentatonic = ""
		
		i = key.index(" ") + 1
		if "Dorian" in key:
			pentatonic = key	
			print(pentatonic)
		elif self.blues == False:
		
			pentatonic = key[:i] + "P-" + key[i:]
		else:
			pentatonic = key[:i] + "PB-" + key[i:]
		
		return pentatonic

	def start_stop_recording(self):
		if self.recording:
			self.recording = False
			self.time = 0
			print("Recording stopped.")
		else:
			self.recording = True
			print("Recording started.")

	def play_chord(self,chord,volume:int = 1,instrument:str="piano",transcription=True):
		#you can add instruments here.

		if instrument == "guitar":
			if transcription:
				chord = self.transcribe_notes(chord)

			for note in chord:
				try:
					sound = pygame.mixer.Sound(f'notes/{note}.mp3')
				except Exception as e:
					print(e)
					
				sound.set_volume(volume)
				sound.play()
				sound.fadeout(1000)

		elif instrument == "violine":

			if transcription:
				chord = self.transcribe_guitar_notes(chord)
			for note in chord:

				sound = pygame.mixer.Sound(f'violine/{note}.wav')				
				sound.set_volume(volume)
				sound.play(maxtime=1500)
				sound.fadeout(1550)
		
		elif instrument == "cello":
			if transcription:
				chord = self.transcribe_guitar_notes(chord)	
			
			for note in chord:

				sound = pygame.mixer.Sound(f'cello/{note}.wav')
				
				sound.set_volume(volume)
				sound.play(maxtime=1500)
				sound.fadeout(1550)
		
		else:
			if transcription:
				chord = self.transcribe_notes(chord)
			
			for note in chord:
				
				sound = pygame.mixer.Sound(f'notes/{note}.mp3')
				sound.set_volume(volume)
				sound.play()   
		
		
		if self.recording:
						
			if len(self.record) == 0:
				self.time = pygame.time.get_ticks()
				self.record.append(chord)
			else:
				
				timePassed = pygame.time.get_ticks() - self.time
				self.record.append(timePassed)
				self.time = pygame.time.get_ticks()
				self.record.append(chord)

	#these are all currently playable chords. Comment those in that you want to have in your digital keyboard.
	def create_all_chords(self):
		allchords = []
		note = 1
		while note < 13:

			allchords.append([self.transcribe_basic_tone(note)] + self.create_major(note))
			allchords.append([self.transcribe_basic_tone(note) + "m"] + self.create_minor(note))
			allchords.append([self.transcribe_basic_tone(note) + "°"] + self.create_diminished(note))
			# allchords.append([self.transcribe_basic_tone(note) + "5"] + self.create_5th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "sus4"] + self.create_suspended_4th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "sus2"] + self.create_suspended_2nd(note))
			# allchords.append([self.transcribe_basic_tone(note) + "(add9)"] + self.create_added_9th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "6"] + self.create_major_6th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "6/9"] + self.create_6th_added_9th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "maj7"] + chords.create_major_7th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "maj9"] + self.create_major_9th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "maj7#11"] + self.create_major_7th_sharp_11th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "maj13"] + self.create_major_13th(note))

			# allchords.append([self.transcribe_basic_tone(note) + "m(add9)"] + self.create_minor_added_9th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "m6"] + self.create_minor_6th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "mb6"] + self.create_minor_flat_6th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "m6/9"] + self.create_minor_6th_added_9th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "m7"] + self.create_minor_7th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "m7b5"] + self.create_minor_7th_flat_5th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "m9"] + self.create_minor_9th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "m11"] + self.create_minor_11th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "m13"] + self.create_minor_13th(note))
			allchords.append([self.transcribe_basic_tone(note) + "7"] + chords.create_dominant_7th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "7sus4"] + self.create_7th_suspended_4th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "9"] + self.create_9th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "9sus4"] + self.create_9th_suspended_4th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "11"] + self.create_11th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "13"] + self.create_13th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "13sus4"] + self.create_13th_suspended_fourth(note))
			# allchords.append([self.transcribe_basic_tone(note) + "+7"] + self.create_augmented_7th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "m(M7)"] + self.create_minor_major_7th(note))
			
			# allchords.append([self.transcribe_basic_tone(note) + "ᵒ7"] + self.create_diminished_7th(note))
			# allchords.append([self.transcribe_basic_tone(note) + "ø7"] + self.create_half_diminished_7th(note))
			note+=1
		
		return allchords

	def create_chord_progression_ONE(self):
		return (0,3,4)

	def create_chord_progression_TWO(self):
		return (0,4,5,3)

	def create_chord_progression_THREE(self):
		return (0,3,0,4,0)

	def create_chord_progression_FOUR(self):
		return (0,5,1,4)

	def create_chord_progression_FIVE(self):
		return (0,1,2,3)

	def create_chord_progression_SIX(self):
		return (0,3)

	def create_chord_progression_SEVEN(self):
		return (0,2,3)

	def create_chord_progression_EIGHT(self):
		return (0,5,3,4)

	def create_chord_progression_NINE(self):
		return (5,3)

	def create_chord_progression_TEN(self):
		return (5,3,4)

	def create_chord_progression_ELEVEN(self):
		return (5,4,3)

	def create_chord_progression_TWELVE(self):
		return (5,3,0,4)

	def create_chord_progression_THIRTEEN(self):
		return (5,1,2)

	def create_chord_progression_FOURTEEN(self):
		return (5,4,1)

	def create_chord_progression_FIFTEEN(self):
		return (5,1,0,4)

	def create_chord_progression_SIXTEEN(self):
		return (3,4,2,5)

	def create_chord_progression_SEVENTEEN(self):
		return (0,11,5,14,3,2,1,4)

	def create_chord_progression_EIGHTEEN(self):
		return (0,11,5,4,3)

	def create_chord_progression_NINETEEN(self):
		return (0,4,5,2)

	def create_chord_progression_TWENTY(self):
		return (0,4,5,7)

	def create_chord_progression_TWENTYONE(self):
		return (0,4,5,2,3)

	def create_chord_progression_CIRCLE_ONE(self):
		return (0,3,6,2,5,1,4,0)

	def create_chord_progression_CIRCLE_TWO(self):
		return (0,3,4,0)

	def create_chord_progression_OVERVIEW(self):
		return (0,1,2,3,4,5,6,7)

	def create_chord_progression_IONIAN_ONE(self):
		return (0,6,3,3)

	def flatten_chord(self,chord):
		
		if chord[0].endswith("m"):			 			
			chord = self.create_minor(chord[1] + 1)
		
		elif chord[0].endswith("°"):
			chord = self.create_diminished(chord[1] + 1)
			
		else:					
			chord = self.create_major(chord[1] + 1)
		
		return chord
		
	def sharpen_chord(self,chord):
		
		if chord[0].endswith("m"):			 
			chord = self.create_minor(chord[1] - 1)

		elif chord[0].endswith("°"):
			chord = self.create_diminished(chord[1] - 1)

		else:			
			chord = self.create_major(chord[1] - 1)
	
		return chord

	def random_chord_progression(self):
		allProgressions = [func for func in dir(Piano) if callable(getattr(Piano, func)) and not func.startswith("__") and func.startswith("create_chord_progression")]
		randomNumber = rd.randint(0,len(allProgressions)-1)
		
		randomProgression = eval("self."+allProgressions[randomNumber])()
		return randomProgression

	def return_all_chord_progessions(self):
		allProgressions = [func for func in dir(Piano) if callable(getattr(Piano, func)) and not func.startswith("__") and func.startswith("create_chord_progression")]
		return allProgressions

	def set_up_piano(self):
		allchords = self.create_all_chords()
		allkeys = self.create_all_keys()

		for chord in allchords:
			for key in allkeys:
				self.check_if_chord_in_key(key,chord)

		for key in self.chordDict:
			i = 0
					
			if key.endswith("- Major"):
				while i < len(self.chordDict[key]):
					if self.chordDict[key][i][0] == key[:2]:
						
						break
					i+=1
			
			elif "Dorian" in key:
				while i < len(self.chordDict[key]):
					if self.chordDict[key][i][0][0] == key[0]:
						break
					i+=1

			elif key.endswith("Major"):
				while i < len(self.chordDict[key]):
					if self.chordDict[key][i][0] == key[0]:
						break
					i+=1

			elif key.endswith("- Minor"):
				while i < len(self.chordDict[key]):
					if self.chordDict[key][i][0] == key[0] +"-m":
						break
					i+=1
				
			elif key.endswith("Minor"):
				while i < len(self.chordDict[key]):
					if self.chordDict[key][i][0] == key[0] + "m":
						break
					i+=1
			elif key.endswith("Persian"):
				while i < len(self.chordDict[key]):
					if self.chordDict[key][i][0] == key[0]:
						break
					i+=1
			

			self.chordDict[key] = self.chordDict[key][i:] + self.chordDict[key][:i]
		
		self.clean_7s()
		self.setUpInversions()
		
	def clean_7s(self):
		
		for key in self.chordDict:
			i = 0
			index = None
			for chord in self.chordDict[key]:
				if "7" in chord[0]:
					break
				i+=1
			self.chordDict[key].append(self.chordDict[key].pop(i))

	def setUpInversions(self):
		
		for key in self.chordDict:
			chordDictKeyCopy = copy.deepcopy(self.chordDict[key])
			for chord in chordDictKeyCopy:
				self.chordDict[key].append((chord[0],chord[2],chord[3],chord[1]+12))
			for chord in chordDictKeyCopy:
				self.chordDict[key].append((chord[0],chord[3],chord[1]+12,chord[3]+12))

	def play_chord_progression_from_key2(self,key):
		progression = self.create_chord_progression_SIXTEEN()

		a = 0
		while a < 50:
			
			i = 0
			while i < len(progression):
				e=0
				deltatime = time.time()
				deltatime1 = time.time()
				
				rhythm = [0.6,0.2,0.4,0.4]
				while e < 4:
					
					self.play_chord(self.chordDict[key][progression[i]],volume = 0.4)						
						
					
					if time.time() - deltatime >= 1.6:								
						tone = rd.randint(1, 3)						
						
					if time.time() - deltatime >= 1.6:								
						tone = rd.randint(1, 3)						
						
					if time.time() - deltatime >= 0.1:		
						tone = rd.randint(1, 3)
						
						self.play_chord([self.keydict[self.find_pentatonic(key)][tone]+12],volume=0.5)
						
						
						deltatime = time.time()
					
					time.sleep(rhythm[e%len(rhythm)])
					e+=1
					
				i+=1
									
			a+=1

	def write_progression(self,key,progression):
		i = 0
	
		while i < len(progression):
			chordName = self.convert_chord_names(self.chordDict[key][progression[i]][0])
			
			if i < len(progression) -1:
				text = font.render(chordName + " |",False,"White")
			else:
				text = font.render(chordName,False,"White")
			
			screen.blit(text,(1+i*115,285))

			i+=1

		i = 0
		pentanonic_length = len(self.keydict[self.find_pentatonic(key)])
		
		while i < pentanonic_length:
			
			noteName = self.transcribe_notes(self.keydict[self.find_pentatonic(key)][i])
			noteName = noteName[0]
			text = font.render("| " + noteName,False,"White")
			screen.blit(text,(950+i*50,285))
			i+=1	
			
	def set_song(self):
		self.screenCount = 0
		self.songKey = self.key
		self.songProgression = self.progression
		self.songProgression = eval("self."+self.songProgression)()

		self.loops = 4
		self.repetitions = 4
		self.chordstep = 0

		self.write_progression(self.songKey,self.songProgression)

	def check_song(self):
		if self.loops > 0:
			
			if time.time() - self.deltatime >= self.rhythmOne[self.chordstep%len(self.rhythmOne)]:
				if self.repetitions == 4:
					self.print_chord(self.chordDict[self.songKey][self.songProgression[self.chordstep]][0],self.chordstep%4)
				
				#edit instrument here if you want to use a different instrument.
				self.play_chord(self.chordDict[self.songKey][self.songProgression[self.chordstep]],volume = 0.4,instrument="Piano")
				
				self.deltatime = time.time()
				self.repetitions -= 1
			
			if self.repetitions == 0:
				self.repetitions = 4
				self.chordstep += 1
			
			if self.chordstep == len(self.songProgression):
				self.chordstep = 0
				self.loops -= 1


	def play_chord_memory(self,key,progression):
		
		progression = eval("self."+progression)()
		
		self.write_progression(key,progression)
		self.draw_text(key)

		rhythm = [0.6,0.2,0.4,0.4]
		slowRhythm = [1.2,0.4,0.8,0.8]
		originalProgression = progression
		originalKey = key
		originalRhythm = rhythm	
		
		a = 0
		while a < 4:
			
			if a % 2 == 0 and a > 0:
				rhythm = [0.4]*4
			
			i = 0
			while i < len(progression):
				
				deltatime = time.time()
				self.print_chord(self.chordDict[key][progression[i]][0],i%4)

				e=0
				while e < 4:
					self.play_chord(self.chordDict[key][progression[i]],volume = 0.4)					
					time.sleep(rhythm[e%len(rhythm)])				
					tone = rd.randint(0, len(self.keydict[self.find_pentatonic(key)])-1)
					self.play_chord([self.keydict[self.find_pentatonic(key)][tone]+12],volume=1,instrument="Piano")

					e+=1 
				i+=1
			a+=1

	def print_chords(self,key,progression):
		i = 0
		while i < len(progression):
			chord = self.chordDict[key][progression[i]][0] 
			print(f'chordpictures/{chord}')
			
			chordImg = pygame.image.load(f'chordpictures/{chord}.png')
			chordImg = pygame.transform.scale(chordImg, (320, 280))
			screen.blit(chordImg,(0,0))
			pygame.display.flip()
			
			i += 1
		
	def print_chord(self,chord,position:int=0):
		try:
			chordImg = pygame.image.load(f'chordpictures/{chord}.png')
			chordImg = pygame.transform.scale(chordImg, (320, 280))
			
			if self.screenCount == 0:
				screen.blit(chordImg,(0,0))
			elif self.screenCount == 1:
				screen.blit(chordImg,(320,0))
			elif self.screenCount == 2:
				screen.blit(chordImg,(640,0))
			elif self.screenCount == 3:
				screen.blit(chordImg,(960,0))
			elif self.screenCount == 4:
				screen.blit(chordImg,(0,height-280-50))
			elif self.screenCount == 5:
				screen.blit(chordImg,(320,height-280-50))
			elif self.screenCount == 6:
				screen.blit(chordImg,(640,height-280-50))
			elif self.screenCount == 7:
				screen.blit(chordImg,(960,height-280-50))
			pygame.display.flip()
		
			self.screenCount += 1
		except Exception as e:
			print(e)
			print(chord)

	def playback(self):
		
		for item in self.record:
			if type(item) == int:
				time.sleep(item/1000)
			else:
				
				self.play_chord(item,transcription=False)

	def draw_text(self,text):
		chord = font.render(text,False,"White")
		color = (0,0,0)
		pygame.draw.rect(screen, color, pygame.Rect(0, height-30, 1300, 30))		
		screen.blit(chord,(1,height-31))
	
	def find_key (self,chords):
		
		if type(chords) == list:
			pass
		elif chords == None:
			chords = input("Enter the chords.")
			self.find_key(chords)
		else:
			chords = chords.split(",")

		potentialList = []
		secondList = []
		thirdList = []

		for key in self.chordDict:
			truthList = []
			for chord in chords:
				i = 0								
				while i < len(self.chordDict[key]):
					
					if chord == self.chordDict[key][i][0]:
						truthList.append(chord)
						
						break
					i+=1
			if len(truthList) == len(chords):
				potentialList.append(key)
			elif len(truthList) == len(chords) - 1:
				secondList.append(key)
			elif len(truthList) == len(chords) - 2:
				thirdList.append(key)
		
		if len(potentialList) > 0:
			print("This is the key:",potentialList)
		elif len(secondList) > 0:
			print("The closest keys are:",secondList)
		else:
			print("These keys have some resemblance",thirdList)

	def switch_blues(self):
		if self.blues == True:
			self.blues = False
		else:
			self.blues = True

		print(self.blues)

p = Piano()	

key = "C Major"
keyNumber = 0
register = 12

progressions = p.return_all_chord_progessions()
current_p = progressions[0]

width, height = 1280, 660
screen = pygame.display.set_mode((width, height))
pygame.display.flip()

font = pygame.font.SysFont("Times New Roman",30)
clock = pygame.time.Clock()
print("Ready to play!")

running = True

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

			if event.key  == pygame.K_1:
				p.play_chord(p.chordDict[p.key][0])
			if event.key  == pygame.K_2:
				p.play_chord(p.chordDict[p.key][1])
			if event.key  == pygame.K_3:
				p.play_chord(p.chordDict[p.key][2])
			if event.key  == pygame.K_4:
				p.play_chord(p.chordDict[p.key][3])
			if event.key  == pygame.K_5:
				p.play_chord(p.chordDict[p.key][4])
			if event.key  == pygame.K_6:
				p.play_chord(p.chordDict[p.key][5])
			if event.key  == pygame.K_7:
				p.play_chord(p.chordDict[p.key][6])
			if event.key  == pygame.K_8:
				p.play_chord(p.chordDict[p.key][7])

			if event.key == pygame.K_r:
				p.start_stop_recording()
			if event.key == pygame.K_x:
				p.record_wav_audio()
				print(p.recorded_chords)
				if len(p.recorded_chords) > 0:
					p.find_key(p.recorded_chords)
		
			if event.key == pygame.K_p:
				playback = threading.Thread(target=p.playback())
				playback.start()

			if event.key  == pygame.K_z:
				p.play_chord([1+p.register])
			if event.key  == pygame.K_u:
				p.play_chord([2+p.register])
			if event.key  == pygame.K_i:
				p.play_chord([3+p.register])
			if event.key  == pygame.K_o:
				p.play_chord([4+p.register])
			if event.key  == pygame.K_h:
				p.play_chord([5+p.register])
			if event.key  == pygame.K_j:
				p.play_chord([6+p.register])
			if event.key  == pygame.K_k:
				p.play_chord([7+p.register])
			if event.key  == pygame.K_l:
				p.play_chord([8+p.register])
			if event.key  == pygame.K_n:
				p.play_chord([9+p.register])
			if event.key  == pygame.K_m:
				p.play_chord([10+p.register])
			if event.key  == pygame.K_COMMA:
				p.play_chord([11+p.register])
			if event.key  == pygame.K_PERIOD:
				p.play_chord([12+p.register])

			if event.key  == pygame.K_MINUS:
				p.register -= 12
				p.draw_text(str(p.register))
			if event.key  == pygame.K_PLUS:
				p.register += 12
				p.draw_text(str(p.register))

			if event.key == pygame.K_LSHIFT:
				tempDict = iter(p.chordDict)
				for entry in tempDict:
					if entry == p.key:
						p.key = next(tempDict,"C Major")				
				p.draw_text(p.key)
			
			if event.key == pygame.K_LCTRL:
				tempList = iter(p.progressions)
				for entry in tempList:
					if entry == p.progression:
						p.progression = next(tempList,p.progressions[0])
				p.draw_text(p.progression)
				
			if event.key == pygame.K_RETURN:
				screen.fill((0,0,0))
				pygame.display.flip()
				p.set_song()
			
			if event.key == pygame.K_SPACE:
				chords = input("Type the chords you want know about.")
				p.find_key(chords)

			if event.key == pygame.K_BACKSPACE:
				p.loops = 0
				screen.fill((0,0,0))
				pygame.display.flip()

			if event.key == pygame.K_b:
				p.switch_blues()

			if event.key  == pygame.K_w:
				screen.fill((0,0,0))
				pygame.display.flip()
				p.play_chord_memory(p.key,p.progression)
				p.screenCount = 0

	p.listen_midi()
	p.play_midi()
	p.check_song()
	pygame.display.update()
	clock.tick(120)