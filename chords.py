print("Chords")
def create_5th(note):
	firstNote = note	
	secondNote = whichNote(note+7)
	return [firstNote,secondNote]

def create_suspended_4th(note):
	firstNote = note
	secondNote = whichNote(note+5)
	thirdNote = whichNote(note+7)
	return [firstNote,secondNote,thirdNote]

def create_suspended_2nd(note):
	firstNote = note
	secondNote = whichNote(note+2)
	thirdNote = whichNote(note+7)
	return [firstNote,secondNote,thirdNote]

def create_added_9th(note):
	firstNote = note
	secondNote = whichNote(note+4)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+14)
	return [firstNote,secondNote,thirdNote,fourthNote]

def create_major_6th(note):
	firstNote = note
	secondNote = whichNote(note+4)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+9)

	return [firstNote,secondNote,thirdNote,fourthNote]

def create_6th_added_9th(note):
	firstNote = note
	secondNote = whichNote(note+4)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+9)
	fifthNote = whichNote(note+14)
	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote]

def create_major_7th(note):
	firstNote = note	
	secondNote = note+4
	thirdNote = note+7
	fourthNote = note+11

	return [firstNote,secondNote,thirdNote,fourthNote]

def create_major_9th(note):
	firstNote = note
	secondNote = whichNote(note+4)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+11)
	fifthNote = whichNote(note+14)
	
	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote]

def create_major_7th_sharp_11th(note):
	firstNote = note
	secondNote = whichNote(note+4)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+11)
	fifthNote = whichNote(note+18)
	
	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote]

def create_major_13th(note):
	firstNote = note
	secondNote = whichNote(note+4)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+11)
	fifthNote = whichNote(note+14)
	sixthNote = whichNote(note+21)
	
	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote,sixthNote]

def create_minor_added_9th(note):
	firstNote = note
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+14)

	return [firstNote,secondNote,thirdNote,fourthNote]

def create_minor_6th(note):
	firstNote = note	
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+9)

	return [firstNote,secondNote,thirdNote,fourthNote]

def create_minor_flat_6th(note):
	firstNote = note
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+8)		
	
	return [firstNote,secondNote,thirdNote,fourthNote]

def create_minor_6th_added_9th(note):
	firstNote = note
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+9)
	fifthNote = whichNote(note+14)
	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote]

def create_minor_7th(note):
	firstNote = note	
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+10)

	return [firstNote,secondNote,thirdNote,fourthNote]

def create_minor_7th_flat_5th(note):
	firstNote = note	
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+6)
	fourthNote = whichNote(note+10)

	return [firstNote,secondNote,thirdNote,fourthNote]

def create_minor_9th(note):
	firstNote = note
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+10)
	fifthNote = whichNote(note+14)
	
	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote]

def create_minor_11th(note):
	firstNote = note
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+10)
	fifthNote = whichNote(note+14)
	sixthNote = whichNote(note+17)
	
	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote,sixthNote]

def create_minor_13th(note):
	firstNote = note
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+10)
	fifthNote = whichNote(note+14)
	sixthNote = whichNote(note+17)
	seventhnote = whichNote(note+21)
	
	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote,sixthNote]

#random chords

def create_dominant_7th(note):
	firstNote = note	
	secondNote = note+4
	thirdNote = note+7
	fourthNote = note+10

	return [firstNote,secondNote,thirdNote,fourthNote]

def create_7th_suspended_4th(note):
	firstNote = note	
	secondNote = whichNote(note+5)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+10)
	return [firstNote,secondNote,thirdNote,fourthNote]

def create_9th(note):
	firstNote = note
	secondNote = whichNote(note+4)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+10)
	fifthNote = whichNote(note+14)
	
	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote]

def create_9th_suspended_4th(note):
	firstNote = note
	secondNote = whichNote(note+5)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+10)
	fifthNote = whichNote(note+14)
	
	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote]

def create_11th(note):
	firstNote = note
	secondNote = whichNote(note+4)
	thirdNote = whichNote(note+10)
	fourthNote = whichNote(note+14) 
	fifthNote = whichNote(note+17)
	
	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote]

def create_13th(note):
	firstNote = note
	secondNote = whichNote(note+4)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+10) 
	fifthNote = whichNote(note+17)
	sixthNote = whichNote(note+21)

	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote,sixthNote]

def create_13th_suspended_fourth(note):
	firstNote = note
	secondNote = whichNote(note+5)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+10) 
	fifthNote = whichNote(note+17)
	sixthNote = whichNote(note+21)

	return [firstNote,secondNote,thirdNote,fourthNote,fifthNote,sixthNote]

def create_augmented_7th(note):
	firstNote = note	
	secondNote = whichNote(note+4)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+9)

	return [firstNote,secondNote,thirdNote,fourthNote]

def create_minor_major_7th(note):
	firstNote = note	
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+7)
	fourthNote = whichNote(note+10)

	return [firstNote,secondNote,thirdNote,fourthNote]

def create_diminished_7th(note):
	firstNote = note	
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+6)
	fourthNote = whichNote(note+9)

	return [firstNote,secondNote,thirdNote,fourthNote]

def create_half_diminished_7th(note):
	firstNote = note	
	secondNote = whichNote(note+3)
	thirdNote = whichNote(note+6)
	fourthNote = whichNote(note+10)

	return [firstNote,secondNote,thirdNote,fourthNote]
