import Live

import Selected_Track_Control.MIDI as MIDI
import Selected_Track_Control.settings as settings
from .Logging import log


from .SessionControl import SessionControl
from .MixerControl import MixerControl
from .GlobalControl import GlobalControl
from .ViewControl import ViewControl
from .DeviceControl import DeviceControl
from .QuantizationControl import QuantizationControl

#def log(self, message):
#	sys.stderr.write("LOG: " + message.encode("utf-8"))

# To avoid a glitch where moving the faders causes a note to sometimes sound on piano midi tracks due to pitch bend,
# Make sure to disable "track" in the midi preferences for this controller and just enable "control"

class SelectedTrackControl:
	__module__ = __name__
	__doc__ = 'MIDI Remote Script to control the selected track'
	__name__ = "SelectedTrackControl MIDI Remote Script"
	
	def __init__(self, c_instance):
		log("SelectedTrackControl::__init__ ========================================")
		self.c_instance = c_instance

		if c_instance:
			self.song = c_instance.song() 
			#self.application = c_instance.application() 

		# flags to track shift buttons
		self.cycle_btn_is_pressed = False # true when Cycle button is down
		self.set_btn_is_pressed = False   # true when Mkr Set button is down
		self.second_btn_was_pressed = False # true when another button was pressed while one of the above was down
		
		#log("hello greg 1")
		# mappings for registered MIDI notes/CCs
		self.midi_callbacks = {}
		
		# lookup object for fast lookup of cc to mode
		self.midi_cc_to_mode = {}
		# parse midi_mapping recursive to process the MIDI.CC mappings
		# (this builds a separate index table specifying a decoder mode for each command)
		self.mapping_parse_recursive(settings.midi_mapping.values())
		
		self._device_control = DeviceControl(c_instance, self)
		
		log("hello greg 2")
		self.components = (
			SessionControl(c_instance, self),
			MixerControl(c_instance, self),
			GlobalControl(c_instance, self),
			ViewControl(c_instance, self),
			self._device_control,
			QuantizationControl(c_instance, self),
		)

		self.fix_cc = 0  # fix for delta CC devices
		self.send_cache = {} # fix for too many MIDI transmissions
		self.send_cache_skip = {}

	def mapping_parse_recursive(self, mapping):
		tuple_type = type((1,2))
		for command in mapping:
			if type(command) == tuple_type:
				self.mapping_parse_recursive(command)
			elif isinstance(command, MIDI.CC):
				#log("MIDI CC %d is %s" % (command.key, command.mode))
				self.midi_cc_to_mode[command.key] = command.mode
		
	
	def suggest_map_mode(self, cc_no):
		#log("suggest_map_mode")
		if cc_no in self.midi_cc_to_mode:
			return self.midi_cc_to_mode[cc_no]
		return MIDI.ABSOLUTE # see MIDI.py for definitions of modes
	
	
	def disconnect(self):
		for c in self.components:
			c.disconnect()
	
	def refresh_state(self):
		#log("refresh_state")
		#for c in self.components:
		#	c.refresh_state()
		pass
	
	def update_display(self):
		#log("update_display")
		#for c in self.components:
		#	c.update_display()
		pass
	
	def connect_script_instances(self, instanciated_scripts):
		pass
	
	def get_unshifted_key(self, key):
		if key > MIDI.SHIFT_SET:
			return key - MIDI.SHIFT_SET
		elif key > MIDI.SHIFT_CYCLE:
			return key - MIDI.SHIFT_CYCLE
		else:
			return key

	# called from Live to build its MIDI bindings
	def build_midi_map(self, midi_map_handle):
		log("SelectedTrackControl::build_midi_map begin")
		script_handle = self.c_instance.handle()
		
		notes_mapped = []
		for channel in range(16):
			callbacks = self.midi_callbacks.get(channel, {})
			
			for note in callbacks.get(MIDI.NOTEON_STATUS,{}).keys():
				#log("NOTE :"  + str(note))
				sh_note = self.get_unshifted_key(note)
				if note != 999 and not (sh_note in notes_mapped):
					log("mapping %s,%s" % (str(note),str(sh_note)))
					Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, channel, sh_note)
					notes_mapped.append(sh_note)
			
			for cc in callbacks.get(MIDI.CC_STATUS,{}).keys():
				#log("CC :"  + str(cc))
				if cc != 999:
					Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, cc)

			for pb in callbacks.get(MIDI.PB_STATUS,{}).keys():
				#log("PB :"  + str(pb))
				if pb != 999:
					Live.MidiMap.forward_midi_pitchbend(script_handle, midi_map_handle, channel)
		log("SelectedTrackControl::build_midi_map end")
		#log("map = %s" % str(notes_mapped))

	def update_transport_leds(self):
		if self.song.is_playing:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_TRANSPORT_PLAY, 127))
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_TRANSPORT_STOP, 0))
		else:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_TRANSPORT_PLAY, 0))
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_TRANSPORT_STOP, 0))
		if self.song.record_mode:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_TRANSPORT_RECORD, 127))
		else:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_TRANSPORT_RECORD, 0))

	def update_track_leds(self):
		track = self.song.view.selected_track
		if track and track.can_be_armed and track.arm:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_RECORD_ARM, 127))
		else:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_RECORD_ARM, 0))
		if track and track.solo:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_SOLO, 127))
		else:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_SOLO, 0))
		if track and track.mute:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_MUTE, 127))
		else:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_MUTE, 0))
		self.send_midi((MIDI.NOTEON_STATUS, 1+settings.SID_SOLO, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 1+settings.SID_MUTE, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 1+settings.SID_RECORD_ARM, 127))
		#self.send_midi((MIDI.NOTEON_STATUS, 2+settings.SID_SOLO, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 2+settings.SID_MUTE, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 2+settings.SID_RECORD_ARM, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 3+settings.SID_RECORD_ARM, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 4+settings.SID_SOLO, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 6+settings.SID_SOLO, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 6+settings.SID_MUTE, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 6+settings.SID_RECORD_ARM, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 7+settings.SID_SOLO, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 7+settings.SID_MUTE, 127))
		self.send_midi((MIDI.NOTEON_STATUS, 7+settings.SID_RECORD_ARM, 127))

	def update_loop_leds(self):
		track = self.song.view.selected_track
		if self.song.loop:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_MARKER_LOOP, 127))
		else:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_MARKER_LOOP, 0))
		if self.song.punch_in:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_TRANSPORT_REWIND, 127))
		else:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_TRANSPORT_REWIND, 0))
		if self.song.punch_out:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_TRANSPORT_FAST_FORWARD, 127))
		else:
			self.send_midi((MIDI.NOTEON_STATUS, settings.SID_TRANSPORT_FAST_FORWARD, 0))

	# called from Live every 100 ms to enable us to update the LEDs
	def update_display(self):
		self.update_transport_leds()
		self.update_track_leds()
		self.update_loop_leds()

	# we send midi codes to light the LEDs on the nanoKontrol
	def send_midi(self, midi_event_bytes):
	#	"""Use this function to send MIDI events through Live to the _real_ MIDI devices
	#	that this script is assigned to."""
		channel = (midi_event_bytes[0] & MIDI.CHAN_MASK)
		status = (midi_event_bytes[0] & MIDI.STATUS_MASK)
		key = midi_event_bytes[1]
		value = midi_event_bytes[2]
		if status == MIDI.NOTEON_STATUS:
			if not key in self.send_cache.keys():
				self.send_cache[key] = value
			elif self.send_cache[key] == value:
				return # don't send message if it has already been sent
			self.send_cache[key] = value
		self.c_instance.send_midi(midi_event_bytes)

	# called from Live when MIDI messages are received
	def receive_midi(self, midi_bytes):
		channel = (midi_bytes[0] & MIDI.CHAN_MASK)
		status = (midi_bytes[0] & MIDI.STATUS_MASK)
		key = midi_bytes[1]
		value = midi_bytes[2]
		
		log("receive_midi on channel %d, status %d, key %d, value %d" % (channel, status, key, value))
		# check button press status
		if status == MIDI.NOTEON_STATUS and key == 86:
			self.cycle_btn_is_pressed = True
			self.second_btn_was_pressed = False
			log("cycle on")
		elif status == MIDI.NOTEOFF_STATUS and key == 86:
			self.cycle_btn_is_pressed = False
			if not self.second_btn_was_pressed:
				if self.set_btn_is_pressed:
					self.song.metronome = not self.song.metronome
				else:
					self.song.loop = not self.song.loop
			log("cycle off")
		elif status == MIDI.NOTEON_STATUS and key == 82:
			log("mkr set on")
			self.set_btn_is_pressed = True
			self.second_btn_was_pressed = False
		elif status == MIDI.NOTEOFF_STATUS and key == 82:
			log("mkr set off")
			self.set_btn_is_pressed = False
		elif status == MIDI.NOTEON_STATUS:
			self.second_btn_was_pressed = True
			if self.set_btn_is_pressed:				
				key = key + MIDI.SHIFT_SET
				log ("key = %s" % key)
			if self.cycle_btn_is_pressed:
				key = key + MIDI.SHIFT_CYCLE
				log ("key = %s" % key)
		
		# execute callbacks that are registered for this event
		callbacks = self.midi_callbacks.get(channel,{}).get(status,{}).get(key,[])
		callbacks_pb = self.midi_callbacks.get(channel,{}).get(status,{}).get(channel,{}) # key not relevant for pitch bends because it contains data
		#log("all = " + str(self.midi_callbacks))
		#log("callbacks = " + str(callbacks))
		#log("callbacks_pb = " + str(callbacks_pb))
		mode = MIDI.ABSOLUTE
		#log("status, key, value = (%s,%s,%s)" % (str(status),str(key),str(value)))
		if status == MIDI.CC_STATUS:
			# look up the mode and calculate signed int for MIDI value
			mode = self.suggest_map_mode(key)
			if value == 2:
				self.fix_cc = 1 # min(self.fix_cc + 1,1000)
			if value == 66:
				self.fix_cc = -1 #self.fix_cc - 1
			#value = MIDI.relative_to_signed_int[mode](value)
			#log("cc,fix = %s,%s" % (str(value),str(self.fix_cc)))
			value = self.fix_cc
		if status == MIDI.PB_STATUS:
			# get mode and calculate signed int for MIDI value
			value = MIDI.relative_to_signed_int[mode](value)
			#log("bend = " + str(value))
			for callback in callbacks_pb:
				log("calling PB " + str(callback))
				callback(value, mode, status)
		else:
			#log("note = " + str(key))
			# handle callbacks
			for callback in callbacks:
				log("calling note  " + str(callback))
				callback(value, mode, status)


	def suggest_input_port(self):
		return str('Kimidi Input')

	def suggest_output_port(self):
		return str('Kimidi Output')

	def can_lock_to_devices(self):
		return True

	def lock_to_device(self, device):
		assert (self._device_control != None)
		self._device_control.set_lock_to_device(True, device)

	def unlock_from_device(self, device):
		assert (self._device_control != None)
		self._device_control.set_lock_to_device(False, device)
	
	def set_appointed_device(self, device):
		assert ((device == None) or isinstance(device, Live.Device.Device))
		assert (self._device_control != None)
		self._device_control.set_device(device)
	
	
	# internal method to register callbacks from different controls
	# creates a list "midi_callbacks" with indices[channel][status][key]
	def register_midi_callback(self, callback, key, mode, status, channel):
		if not channel in self.midi_callbacks:
			self.midi_callbacks[channel] = {}
		
		if not status in self.midi_callbacks[channel]:
			self.midi_callbacks[channel][status] = {
				key: [callback,]
			}
		else:
			if key in self.midi_callbacks[channel][status]:
				self.midi_callbacks[channel][status][key].append(callback)
			else:
				self.midi_callbacks[channel][status][key] = [callback, ]
	