This is very clumsy and rudimentary digital audio workstation that mainly allows you to plugin a midi keyboard and play chord progressions based on single notes that you have to provide yourself.
No Audio Edititing. 

Chord Progression Playback
Real Audio Recording
Digital Audio Recording (of the buttons pressed in the DAW)


# Dependencies

```bash
pip install pygame
pip install Pillow

```


# Provide your own audio
Due to copyright reasons you'll have to provide your own audio.
In order to get this software working, check out the picture inn the notes folder.
There you'll see how the notes have to be arranged.
Notably there is no flat note annotation, thus "a3" is a lower pitched "a" and "a-3" is the sharp variation of that "a" and so on. "b♭" is annotated as "a-" in this software.
You don't need to provide as many sounds as in the example for the programm to work (or not to crash rather) it'll just play nothing if it can't find the file.
In my case all the soundfiles are about 1 second long but you can obviously variate this.

# Manual

Once you have the audio files setup and the dependencies installed, run main.py.
This will open a black pygame screen that you can navigate with the following keys.

Shift | Switches key. The programm always starts in C Major.

CTRL | Switches Chord Progression (These are named horribly you just have to go through them and see which you liked).

Enter | Plays a tune in the current key and chord progression and displays the currently played progression with guitar annotation. (this really is the coolest and best working feature of this software.

Backspace | Stops the the tune you started with Enter.

Escape | Closes the programm.

Numbers 1-7 | Play the first, second, third chord of the currently selected key. So in C-Major Key 1 plays a C-Major Key 2 plays a D-Minor and so on.

Space | You can type in a couple of chords (in the terminal, not the pygame window) and it'll tell you which key they are in.

z | Plays 'c'

u | Plays 'c-'

i | Plays 'd'

o | Plays 'd-'

h | Plays 'e'

j | Plays 'f'

k | Plays 'f-'

l | Plays 'g'

n | Plays 'g-'

m | Plays 'a'

, | Plays 'a-'

. | Plays 'b'

r | Records your the input that you play with your numberkeys, the Z to . notes or a connected midikeyboard. Press r again to stop the recording.

p | Plays the playback of your recording of r.

\+ | Moves up all the single notes an octave.

\- | Moves down all the single notes an octave.

x | Experimentally records audio through your microphone and tells you the chords you played and the corresponding key.  (you'll have to check the record_wav_audio function and edit line 90 to the name of your microphone for this to work)

b | Switches the programm into blues mode.

# Midi Keyboard Setup.

Connect your midi keyboard to your computer and make sure it's setup properly.
Then open main.py and edit line 56 in the setup_midi_keyboard function and change "Vortex Wirelles 2" in the line
```python
if entry == "Vortex Wireless 2":
```
to the name of your keyboard.

The coolest thing you can do with a keyboard connected is select a key, press enter and then jam your heart out with your keyboard.

If you have any questions don't hesitate to open an issue!
