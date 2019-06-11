import mido
import time
import sys

class PianoListener:
 def __init__(self):
  time.clock()
  self.port = PianoListener.get_port()
  self.log = open('log.csv', 'a+')

 @staticmethod
 def get_port(port_name=u'USB func for MIDI:USB func for MIDI MIDI 1 36:0'):
  port_names = mido.get_output_names()
  print port_names
  if not port_name in port_names:
   for port_name in port_names:
    if 'USB func for' in port_name:
     break
  port = mido.open_input(port_name)
  return port

 def __iter__(self):
  for message in self.port:
   yield message

 def listen(self):
  for message in self:
   self.handle_message(message)

 def handle_message(self, message):
  if message.type == 'note_on':
   if message.note == 108:
    self.log.close()
    sys.exit()
   log_line = ' '.join(map(str, (message.note, self.now(), '\n')))
   print log_line,
   self.log.write(log_line)

 def now(self):
  return time.clock()

def main():
 piano_listener = PianoListener()
 piano_listener.listen()

if __name__ == '__main__':
 main()
