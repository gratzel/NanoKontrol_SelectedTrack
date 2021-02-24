import Selected_Track_Control.MIDI as MIDI
import Selected_Track_Control.settings as settings
from .Logging import log

class Control:
#	__module__ = __name__
	__doc__ = "Super-class for Controls"

	def __init__(self, c_instance, selected_track_controller):
		log ("control init")
		self.c_instance = c_instance
		if c_instance:
			self.song = c_instance.song()
			#self.application = c_instance.application() 
		self.selected_track_controller = selected_track_controller
		#self.midi_callbacks = (,)
		
		
		for key, callback in self.get_midi_bindings():
			if not key in settings.midi_mapping:
				log("no mapping for control '%s' - see settings.py" % key)
				continue
			
			mapping = settings.midi_mapping[key]
			# always make sure mapping is a tuple
			if isinstance(mapping, MIDI.MIDICommand):
				mapping = (mapping,)
			
			for m in mapping:
				if m.key != 999:
					log("status = %s, key = %s, mode = %s, channel = %s" % (m.status,m.key,m.mode,m.channel))
					self.selected_track_controller.register_midi_callback(callback, m.key, m.mode, m.status, m.channel)
				
	
	def disconnect(self):
		pass
	
	def get_midi_bindings(self):
		return set() # return an empty set here, 
		# but in each subclass, it contains a set of callbacks and keys that trigger them
	
	def show_message(self, msg):
		""" display msg in Live's status bar """
		assert isinstance(msg, (str, unicode))
		self.c_instance.show_message(msg)

	def send_midi(self, bytes):
		self.selected_track_controller.send_midi(bytes)
