NanoKontrol Mod Selected Track Control for Ableton Live
=======================================

Current version is 1.0 – released Feb 28, 2021.  
Compatible with Live 11 (does not work with previous versions)

![alt text](https://github.com/gratzel/Selected_Track_Control/blob/main/nanokontrol%20picture.jpg?raw=true)

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
*	TRACK LEFT = undo
*	TRACK RIGHT = redo
*	CYCLE = loop toggle 
*	<< = punch-in, shift to move loop selection
*	>> = punch-out, shift to move loop selection
*	STOP = toggle play/stop
*	PLAY = toggle play/pause
*	REC = toggle record arm (shift to toggle overdub)
*	SET = shift
*	MARKER LEFT = zoom in (shift to scroll)
*	MARKER RIGHT = zoom out (shift to scroll)

*	SH+PLAY = continue
*	SH+REC = automation arm
*	SH+TRACK < = jog view left (check out on_cursor_up_pressed)
*	SH+TRACK > = jog view right (or also set punch-out point)
*	SH+CYCLE = metronome
*	SH + MARKER < = undo
*	SH + MARKER > = redo

*	Mixer 1
    *	S = solo selected track (shift for exclusive)
    *	M = mute
    *	R = toggle track rec (shift for exclusive)
    *	Fader = track volume
    *	Knob = send @1

*	Mixer 2
    *	S = prev track
    *	M = toggle in/auto
    *	R = next track
    *	Fader = pan
    *	Knob = send #2

*	Mixer 3
    *	S = collapse all tracks
    *	M = collapse selected track 
    *	R = toggle device/clip view
    *	Fader = 
    *	Knob = send #3

*	Mixer 4
    *	R = Force clip to loop
    *	Fader = clip gain

*	Mixer 5
    *	S = Tap Tempo

*	Mixer 6
    *	Fader = cue level

*	Mixer 7
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

### Version 1.2.9 (released May 15, 2013) ###

Added compatibility for Live 9


### Version 1.2.8 (released Sept 26, 2012) ###

Added dedicated tart, stop and continue-playing commands - this is useful for e.g. hitting stop 3 times in row for MIDI panic functionality  
Fixed scrub/rewind bug


### Version 1.2.7 (released Mar 14, 2012) ###

Added select scene/track by number directly by MIDI value  
Added toggle selected clipslot play/stop


### Version 1.2.6 (released Feb 7, 2012) ###

Added support for back-to-arranger button.


### Version 1.2.5 (released Nov 18, 2011) ###

Added toggle to fold/unfold automation lane in Arrangement.


### Version 1.2.4 (released Nov 14, 2011) ###

Added crossfader assignment and control. Added cue volume.
Fixed tracks navigation when group track is folded.


### Version 1.2.3 (released Sept 29, 2011) ###

Added notes and absolute MIDI CC triggers for quantization control


### Version 1.2.2 (released Sept 27, 2011) ###

Added quantization control - control MIDI recording quantization and clip launch quantization via MIDI.


### Version 1.2.1 (released Aug 17, 2011) ###

Added View control - select which main views are visible in the GUI (Browser, Session/Arrangement, Detail Clip/Devices)
Added ParamSetter for custom Device-handlers. Currently only Looper has a custom handler for its "State"-parameter. Note though, that Looper’s API support is very limited. Using Looper via _MIDI Remote Scripts_ is only useful if you are already in play mode (so no set-tempo functionality) and if you record for a predefined length.


### Version 1.2 (released Aug 8, 2011) ###

Added Device selection and control


### Version 1.1.8 (released Jun 22, 2011)

Auto-arm track on selection now works when using the mouse! 
Added _scrubbing_ in Arrangement-View as well as _select playing clip-slot_ in Session-View.


### Version 1.1.7 (released Jun 16, 2011)

made CCs for toggled elements behave like Note (so ignore zero-values) – this is useful for pad-controllers, that also send CCs like the LPD8.
improved auto-arm on selection if STC.app is used – thanks to new MIDI-loopback functionality in STC.app, auto-arm now works when selecting the track via mouse too! As a default has\_midi\_loopback is deactivated.


### Version 1.1.6 (released Apr 21, 2011)

added global DEFAULT_CHANNEL to easily make STC listen on another MIDI channel


### Version 1.1.5 (released Apr 14, 2011)

made settings optional (so you don’t have to define all controls for Live – useful if you use STC for your own MIDI controller)


### Version 1.1.4 (released Mar, 2011)

no changes, just matching release number for Selected Track Control.app (which added support for only being active when Live is front-most app)


### Version 1.1.3 (released Feb 19, 2011)

Fixed and added some global controls (play/pause/play selection as well as undo/redo), added stop-controls to selected and all tracks


### Version 1.1.2 (released Feb 18, 2011)

Improved Session-Navigation:

*	Walk through tracks/scenes via MIDI Note-events (Notes 82-85)
*	Navigate tracks/scenes with absolut MIDI CC (tracks/scenes are distributed evenly across the whole range of 0-127)


### Version 1.1.1 (released Feb 17, 2011)

Small bugfix concerning absolute MIDI CC controlling volume, pan, etc.


### Version 1.1 (released Feb 16, 2011)

Added several new features such as:

*	**Auto-arm on selection** arms a track automatically when selected through STC
*	**Solo kill** deactivates any active soloing on any track independent of the track your on
*	**Mute flip** mutes active tracks and unmutes muted tracks
*	**Tap Tempo** (Live 8 only) instantly mapped – no previous manual mapping required

Made STC more versatile by supporting a wider range of MIDI commands (use it with your own MIDI controller!)

*	**Support for absolute and relative MIDI CC values** (7-bit only) – no more rel2comp-bindings; feel free to use STC with your custom MIDI controller! Some default MIDI CC bindings already pre-defined – for more info see MIDI Implementation Chart
*	**Unlimited sends** – control effect-level to as many sends as you need, you are only limited by your MIDI controller (using keyboard shortcuts only sends 1-4 are available)


### Version 1.0.1 (released June 7, 2010)

This is a maintenance release. The following items were fixed and/or added:

*	fixed panning issue (panning left was broken)
*	added version numbers and changelog


### Version 1.0 (released May 28, 2010)

First public release.
