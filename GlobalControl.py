import Selected_Track_Control.MIDI as MIDI
import Selected_Track_Control.settings as settings
from .Logging import log
import Live

from .Control import Control

class GlobalControl(Control):
#	__module__ = __name__
	__doc__ = "Global parameters of SelectedTrackControl"

	def __init__(self, c_instance, selected_track_controller):
		log ("global control init")
		Control.__init__(self, c_instance, selected_track_controller)
		
		# steps, when ABSOLUTE mode for tempo CC is used
		self.tempo_step = (settings.tempo_max - settings.tempo_min)/127.0
		
	
	def get_midi_bindings(self):
		return (
			("automation", self.toggle_automation),
			("overdub", self.toggle_overdub),
			("disable_overdub", self.disable_overdub),
			("record", self.toggle_record),
			("back_to_arranger", self.back_to_arranger),
			
			("punch_in", self.toggle_punchin),
			("punch_out", self.toggle_punchout),
			
			("metronome", self.toggle_metronome),
			("loop", self.toggle_loop),
			("count_in_off", self.count_in_off),
			("count_in_on", self.count_in_on),
					
			("loop_move", self.move_loop_by),
			("loop_move_left", self.move_loop_left),
			("loop_move_right", self.move_loop_right),
			("loop_rb_move", self.move_loop_right_bracket_by),
			("loop_lb_move", self.move_loop_left_bracket_by),
			("loop_rb_move", self.move_loop_right_bracket_by),
			("scroll_left", self.scroll_left),
			("scroll_right", self.scroll_right),
			("zoom_in", self.zoom_in),
			("zoom_out", self.zoom_out),
			("tempo", self.set_tempo),
			("tempo_increase", lambda value, mode, status : self.set_tempo(1, MIDI.RELATIVE_TWO_COMPLIMENT, status)),
			("tempo_decrease", lambda value, mode, status : self.set_tempo(-1, MIDI.RELATIVE_TWO_COMPLIMENT, status)),
			("tap_tempo", self.tap_tempo),
			
			("play_stop", self.play_stop),
			("play_pause", self.play_pause),
			("play_selection", self.play_selection),
			("stop_playing", self.stop_playing),
			("start_playing", self.start_playing),
			("continue_playing", self.continue_playing),
			
			("scrub_by", self.scrub_by),
			("scrub_forward", lambda value, mode, status : self.scrub_by(settings.scrub_increment, MIDI.RELATIVE_TWO_COMPLIMENT, status)),
			("scrub_rewind", lambda value, mode, status : self.scrub_by(-settings.scrub_increment, MIDI.RELATIVE_TWO_COMPLIMENT, status)),
			
			("undo", self.undo),
			("redo", self.redo),
			
			("toggle_track_collapsed", self.toggle_track_collapsed),
			("toggle_track_view", self.toggle_track_view),
		)
	
	def toggle_automation(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		#self.song.session_automation_record = not self.song.session_automation_record

	def count_in_off(self, value, mode, status): # turns out not settable :-(
		self.song.count_in_duration = 0
	def count_in_on(self, value, mode, status):
		self.song.count_in_duration = 1

	def zoom_out(self, value, mode, status):
		view = Live.Application.get_application().view
		view.zoom_view(2, 'Arranger', False)
	def zoom_in(self, value, mode, status):
		view = Live.Application.get_application().view
		view.zoom_view(3, 'Arranger', False)

	def scroll_left(self, value, mode, status):
		#self.song.jump_by(-16)
		view = Live.Application.get_application().view
		view.scroll_view(2, 'Arranger', False)
	def scroll_right(self, value, mode, status):
		#nav = Live.Application.Application.View.NavDirection
		view = Live.Application.get_application().view
		view.scroll_view(3, 'Arranger', False)

	def toggle_track_view(self, value, mode, status):
		view = Live.Application.get_application().view
		if view.is_view_visible('Detail/DeviceChain'):
			view.show_view('Detail/Clip')
		else:
			view.show_view('Detail/DeviceChain')

	def toggle_track_collapsed(self, value, mode, status):
		# ignore CC toggles (like on LPD8)
		if status == MIDI.CC_STATUS and not value:
			return
		
		track_view = self.song.view.selected_track.view
		
		if status == MIDI.NOTEON_STATUS:
			# toggle
			track_view.is_collapsed = not track_view.is_collapsed
		else:
			if mode == MIDI.ABSOLUTE:
				if value == 127:
					# CC toggle (like on LPD8)
					track_view.is_collapsed = not track_view.is_collapsed
				elif value > 63:
					track_view.is_collapsed = True
				else:
					track_view.is_collapsed = False
			else:
				if value > 0:
					track_view.is_collapsed = True
				else:
					track_view.is_collapsed = False
	
	def scrub_by(self, value, mode, status):
		self.song.scrub_by(value)

	def stop_playing(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		self.song.stop_playing()
	def start_playing(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		self.song.start_playing()
	def continue_playing(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		self.song.continue_playing()

	
	def play_stop(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		if self.song.is_playing:
			self.song.stop_playing()
		else:
			self.song.start_playing()
	
	def play_pause(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		if self.song.is_playing:
			self.song.stop_playing()
		else:
			if self.song.record_mode:
				self.song.start_playing()
			else:
				self.song.continue_playing()
	
	def play_selection(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value: # ignore 0 values from CC-pads
			return
		#if self.song.is_playing:
		#	self.song.stop_playing()
		#else:
		self.song.play_selection()
	
	def undo(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.undo()
	
	def redo(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.redo()
			
	def toggle_overdub(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.arrangement_overdub = not self.song.arrangement_overdub
	
	def disable_overdub(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.overdub = 0
	
	def back_to_arranger(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.back_to_arranger = 0
	
	def toggle_record(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.record_mode = not self.song.record_mode
	def toggle_punchin(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.punch_in = not self.song.punch_in
	def toggle_punchout(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.punch_out = not self.song.punch_out
		
	def toggle_metronome(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.metronome = not self.song.metronome
	
	def toggle_loop(self, value, mode, status):
		#log("status,value = %s,%s" % (str(status), str(value)))
		if status == MIDI.CC_STATUS and not value:
			return
		self.song.loop = not self.song.loop
		
	def move_loop_left(self, value, mode=None, status=None):
		# only process move if shift button is pressed
		#if self.selected_track_controller.set_btn_is_pressed:
		if self.song.punch_in or not (self.song.punch_in or self.song.punch_out):
			self.move_loop_left_bracket_by(-4)
		if self.song.punch_out or not (self.song.punch_in or self.song.punch_out):
			self.move_loop_right_bracket_by(-4)

	def move_loop_right(self, value, mode=None, status=None):
		# only process move if shift button is pressed
		#if self.selected_track_controller.set_btn_is_pressed:
		if self.song.punch_in or not (self.song.punch_in or self.song.punch_out):
			self.move_loop_left_bracket_by(4)
		if self.song.punch_out or not (self.song.punch_in or self.song.punch_out):
			self.move_loop_right_bracket_by(4)

	def move_loop_by(self, value, mode=None, status=None):
		self.song.loop_start = self.song.loop_start + value

	def move_loop_left_bracket_by(self, value, mode=None, status=None):
		self.move_loop_by(value, mode, status)
		self.move_loop_right_bracket_by(-value, mode, status)
	
	def move_loop_right_bracket_by(self, value, mode=None, status=None):
		self.song.loop_length = self.song.loop_length + value
	
	def set_tempo(self, value, mode, status):
		if mode == MIDI.ABSOLUTE:
			self.song.tempo = settings.tempo_min + value*self.tempo_step
		else:
			self.song.tempo = self.song.tempo + value
	
	def tap_tempo(self, value, mode, status):
		if status == MIDI.CC_STATUS and not value:
			return
		if self.song.tap_tempo:
			self.song.tap_tempo()