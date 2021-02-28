NanoKontrol Mod Selected Track Control for Ableton Live
=======================================

Current version is 1.0 – released Feb 28, 2021.  
Compatible with Live 11 (does not work with previous versions)

![alt text](https://github.com/gratzel/NanoKontrol_SelectedTrack/blob/main/nanokontrol%20picture.jpg?raw=true)

This project is a derivative of [Selected Track Control](http://stc.wiffbi.com/) that provide functionality I found more useful than the original, specifically to optimize for use in Session View (I rarely use Clip View).  It also works in Live 11, which required porting the original to Python 3.

Control the currently selected track via common MIDI messages
-------------------------------------------------------------

NanoKontrol Mod is a *MIDI Remote Script* for Ableton Live, that gives access to common settings of the currently selected track (arm, mute, solo, volume, pan, etc.) via common MIDI messages. Furthermore some global controls are instantly mapped as well.

Among the mapped functionality is:

*	**arm** (record-enable), **solo** and **mute** the selected track
*	control **volume, pan** and **send 1-4** of the selected track
*	**toggle monitoring** from On, In, Off the selected track
*	**toggle metronom, overdub, punch-in, punch-out, record** without having to manually assign them
*	**tap tempo**
*	**navigate session-view** without it having focus (up/down, left/right, first/last)
*	…

Specifically, the controls are:
*	**TRACK LEFT** = undo
*	**TRACK RIGHT** = redo
*	**CYCLE** = loop toggle 
*	**<<** = punch-in, shift to move loop selection
*	**\>\>** = punch-out, shift to move loop selection
*	**STOP** = toggle play/stop
*	**PLAY** = toggle play/pause
*	**REC** = toggle record arm (shift to toggle overdub)
*	**SET** = shift
*	**MARKER LEFT** = zoom in (shift to scroll)
*	**MARKER RIGHT** = zoom out (shift to scroll)

*	**SH+PLAY** = continue
*	**SH+REC** = automation arm
*	**SH+TRACK <** = jog view left (check out on_cursor_up_pressed)
*	**SH+TRACK \>** = jog view right (or also set punch-out point)
*	**SH+CYCLE** = metronome
*	**SH + MARKER <** = undo
*	**SH + MARKER >** = redo

*	**Mixer 1**
    *	S = solo selected track (shift for exclusive)
    *	M = mute
    *	R = toggle track rec (shift for exclusive)
    *	Fader = track volume
    *	Knob = send @1

*	**Mixer 2**
    *	S = prev track
    *	M = toggle in/auto
    *	R = next track
    *	Fader = pan
    *	Knob = send #2

*	**Mixer 3**
    *	S = collapse all tracks
    *	M = collapse selected track 
    *	R = toggle device/clip view
    *	Fader = 
    *	Knob = send #3

*	**Mixer 4**
    *	R = Force clip to loop
    *	Fader = clip gain

*	**Mixer 5**
    *	S = Tap Tempo

*	**Mixer 6**
    *	No mapping

*	**Mixer 7**
    *	Fader = cue level

*	**Mixer 8**
    *	Fader = master volume level



License
-------------------
I guess this work is licensed under the "Simplified BSD License" / "FreeBSD License"
see License.txt


System Requirements
-------------------
Ableton Live 11




Installation
------------

Download the directory into C:\ProgramData\Ableton\Live 11 Suite\Resources\MIDI Remote Scripts.

1.	Stop Live if it is running.
2.	Copy the folder to *Selected_Track_Control* to Ableton Live's MIDI Remote Scripts
3.	Start Live.
4.	Enable **Selected Track Control** as a Control Surface in Live

	In Live’s Preferences go to the *MIDI Sync* tab and select *Selected Track Control* in the dropdown list of available Control Surfaces. As MIDI Input select your controller’s MIDI-port. A MIDI Output is not needed.
	



Customize MIDI messages
-----------------------

The MIDI message, which **Selected Track Control** reacts upon, are defined in settings.py

You can change them there to match your needs, but be careful not to use the same note- or CC-number twice as this might result in unexpected behaviour.



Changelog
---------

### Version 1.0 (released Feb 28 2021) ###

Initial release



