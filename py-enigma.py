#!/usr/bin/python
#
#   py-enigma
#
#   An enigma machine simulator.
#
#   This program is free software: you can redistribute it and/or modify it
#   under  the terms of the GNU General Public License as published by  the
#   Free Software Foundation, either version 3 of the License, or (at  your
#   option) any later version.
#
#   This  program  is distributed in the hope that it will be  useful,  but
#   WITHOUT   ANY   WARRANTY;  without  even  the   implied   warranty   of
#   MERCHANTABILITY  or  FITNESS  FOR A PARTICULAR  PURPOSE.  See  the  GNU
#   General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <http://www.gnu.org/licenses/>.
#                       
#   Requires:         - sys, os
#
#   19 Dec 24   0.1   - Initial version - MT
#   25 Dec 24   0.2   - Added command line parsing (implemented without the 
#                       use of argparse or optargs to keep any dependencies
#                       to a minimum - MT
#                     - The text and initial rotor positions are now passed
#                       from the command line - MT
#                     - Improved verbose output - MT
#                     - Steps the next rotor after the position reaches the
#                       notch on the current rotor (need to fix the  double
#                       stepping behaviour of the M3 or M4) - MT
#   29 Dec 24   0.3   - Reduced the level of verbosity to a single level of
#                       detail (it is now all or nothing) - MT
#                     - Map the specified wiring of each rotor to the input
#                       and output paths using a lookup table, which allows
#                       the  ring position (ringstellung) to be  configured
#                       when a rotor is initialised - MT
#   30 Dec 24   0.4   - Added  a plug board (steckerbrett) by using a rotor
#                       to exchange pairs of letters - MT
#                     - The initial ring positions can now be specified  on 
#                       the command line - MT
#                     - Added a name property to the rotor class - MT
#                     - Fixed wheel stepping - MT
#                     - Rotors  can have multiple turnover positions  which 
#                       allows the use of rotors VI VII and VIII - MT
#                     - Fixed small bug in verbose output - MT
#   03 Jan 25   0.5   - The plug board settings can now be specified on the
#                       command line as a comma delimited list - MT
#                     - Removed name property to the rotor class (since the
#                       rotors are now defined in a dictionary) - MT
#   04 Jan 25         - Allows  the position of each rotor to be fixed.  If
#                       the  turnover isn't defined then the rotor will  be
#                       fixed by default - MT
#                     - Reversed the order in which the rotors are  defined
#                       when setting up the Enigma object - MT
#   05 Jan 25         - Rotors can be selected from the command line - MT
#                     - Ignores options that require parameters if none are
#                       specified on the command line - MT
#
#   To Do:            - Allow the user to specify the reflector.
#                     - Add more validation.
#

_VERSION = "0.5"

def _about():
  sys.stdout.write("Usage: " + sys.argv[0] + "[OPTION]... [FILE]...\n"
    "Decodes binary arguments.\n" + "\n" +
    "  -w, --rotors N,N,N,A         selects the rotors (default III, II, I)\n" +
    "  -s, --settings AAA           set the initial rotor positions\n" +
    "  -r, --rings AAA              set the initial ring positions\n" +
    "  -p, --plugboard AA[,AA...]   specify the plug-board settings (max 10 pairs of letters)\n" +
    "  -v, --verbose                verbose output\n" +
    "  -?, --help                   display this help and exit\n" +
    "      --version                output version information and exit\n\n" +
    "Example:\n" +
    "  " + os.path.basename(sys.argv[0]) + " -w III,II,I -s OKW ENIGMA\n")
  raise SystemExit

def _version():
  sys.stdout.write(os.path.basename(sys.argv[0]) + " " + str(_VERSION) +"\n"
    "License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.\n"
    "This is free software: you are free to change and redistribute it.\n"
    "There is NO WARRANTY, to the extent permitted by law.\n")
  raise SystemExit

def _error(_error):
  sys.stderr.write(os.path.basename(sys.argv[0]) + ": " + _error + "\n")
  raise SystemExit

class Rotor:
  def __init__(self, wiring = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", turnover = None):
    self.wiring = list(wiring)
    self.ring = 0
    self.position = 0
    self.turnover = [False] * 26
    if turnover is None: # If the turnover isn't defined then the rotor will be fixed by default.
      self.fixed = True
    elif turnover.isalpha(): 
      self.fixed = False
      for _char in turnover.upper():
        self.turnover[ord(_char.upper()) - 65] = True
    else:
      _error("rotor turnover positions must be alphabetic")
    self.inp = [None] * 26
    for _count, _char in enumerate(self.wiring):
      self.inp[_count] = ord(_char) - 65
    self.out = [None] * 26
    for _count, _value in enumerate(self.inp):
      self.out[_value] = _count

  def forward(self, char):
    _shift = (ord(char) - 65 + self.position - self.ring ) % 26
    _output = self.inp[_shift]
    if _verbose > 0: sys.stdout.write(chr((ord(char) - 65 + self.position) % 26 + 65) + "->" + chr((_output + 26 + self.ring) % 26 + 65) + "; ")
    return chr((_output + 26 - self.position + self.ring) % 26 + 65)

  def backward(self, char):
    _shift = (ord(char) - 65 + self.position - self.ring ) % 26
    _output = self.out[_shift]
    if _verbose > 0: sys.stdout.write(chr((ord(char) - 65 + self.position) % 26 + 65) + "->" + chr((_output + 26 + self.ring) % 26 + 65) + "; ")
    return chr((_output + 26 - self.position + self.ring) % 26 + 65)

  def rotate(self):
    _rotate = self.turnover[self.position]
    if not self.fixed: self.position = (self.position + 1) % 26 # Move rotor by one step.  
    return _rotate # Return true if position matched notch

  @property    
  def fixed(self):
    return self.fixed
    
  @fixed.setter
  def fixed(self, state):
    self.fixed = state
    return self.fixed


class Enigma:
  def __init__(self, plugboard, reflector, rotors, state, rings):
    self.plugboard = plugboard
    self.rotors = list(reversed(rotors))
    self.reflector = reflector
    self.reset(state, rings)

  def reset(self, state, rings):
    for rotor, position in zip(self.rotors, reversed(state)):
      rotor.position = ord(position) - 65
    for rotor, ring in zip(self.rotors, reversed(rings)):
      rotor.ring = ord(ring) - 65

  def encrypt(self, message):
    result = ""
    for char in message.upper():
      if char.isalpha():
        self.rotate_rotors()
        if _verbose > 0: 
          for rotor in reversed(self.rotors):
            sys.stdout.write(chr(rotor.position + 65))
          sys.stdout.write(" " + char + " ")
        char = self.plugboard.forward(char)
        for rotor in self.rotors:
          char = rotor.forward(char)
        char = self.reflector.forward(char)
        for rotor in reversed(self.rotors):
          char = rotor.backward(char)
        char = self.plugboard.backward(char)
        if _verbose > 0: sys.stdout.write(char + "\n")
        result += char
      else:
        result += char
    return result

  def rotate_rotors(self):
    if self.rotors[1].turnover[self.rotors[1].position]: # Check for 2nd rotor stepping.
      if self.rotors[1].rotate():
        self.rotors[2].rotate()
    _rotate = True # Always moves the first rotor.
    for _rotor in self.rotors:
      if _rotate: 
        _rotate = _rotor.rotate()


if __name__ == '__main__':

  import sys, os

  _text = []
  _settings = "AAA"
  _rings = "AAA"
  _verbose = 0
  _count = 1

  _rotor = {}
  _rotor['I'] =     Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
  _rotor['II'] =    Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
  _rotor['III'] =   Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
  _rotor['IV'] =    Rotor("ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J')
  _rotor['V'] =     Rotor("VZBRGITYUPSDNHLXAWMJQOFECK", 'Z')
  _rotor['VI'] =    Rotor("JPGVOUMFYQBENHZRDKASXLICTW", 'ZM')
  _rotor['VII'] =   Rotor("NZJHGRCXMYSWBOUFAIVLPEKQDT", 'ZM')
  _rotor['VIII'] =  Rotor("FKQHTLXOCBJSPDZRAMEWNIUYGV", 'ZM')

  _reflector = {}
  _reflector['A'] = Rotor("EJMZALYXVBWFCRQUONTSPIKHGD", None) # Reflector 'A'
  _reflector['B'] = Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT", None) # Reflector 'B'
  _reflector['C'] = Rotor("FVPJIAOYEDRZXWGCTKUQSBNMHL", None) # Reflector 'C'

  _rotors = [_rotor['III'], _rotor['II'], _rotor['I']]
  _selected = _reflector['B']
  _plugboard =   Rotor() # Create an empty plugboard (steckerbrett)

  while _count < len(sys.argv):
    _arg = sys.argv[_count]
    if _arg[:1] == "-" and len(_arg) > 1:
      if _arg in ["--verbose", "-v"]:
        _verbose += 1
      elif _arg in ["--setting","-s"]:
        if (_count + 1) < len(sys.argv) and sys.argv[_count + 1][0] != "-": # Check argument given
          _count += 1
          _settings = sys.argv[_count].upper()
          if not(_settings.isalpha() and len(_settings) == 3):
            _error("invalid rotor setting")
      elif _arg in ["--ring","-r"]:
        if (_count + 1) < len(sys.argv) and sys.argv[_count + 1][0] != "-": # Check argument given
          _count += 1
          _rings = sys.argv[_count].upper()
          if not(_rings.isalpha() and len(_rings) == 3):
            _error("invalid ring setting")
      elif _arg in ["--plugboard","-p"]:
        if (_count + 1) < len(sys.argv) and sys.argv[_count + 1][0] != "-": # Check argument given
          _count += 1
          _option = ''
          _next = ','
          while _count < len(sys.argv) and (_next == ','): # Read comma separated list of settings from the command line
            _option += sys.argv[_count].upper()
            _next = _option.strip()[-1:]
            _option = _option.replace(' ','') # Remove any spaces
            _count += 1
            if _next != ',' and _count < len(sys.argv): # Look ahead
              _next = sys.argv[_count].upper().strip()[-1:]
          _count -= 1
          for _each in _option.split(','): # Validate plug-board settings
            if not(_each.isalpha() and len(_each) == 2): # Check each setting is 2 alphabetic characters 
              _error("invalid plugboard setting") 
          _option = _option.replace(',','')
          if len(_option) > 20: # Up to a maximum of 10 letters can be exchanged using the plug-board
            _error("not enough cables")
          if len(set(_option)) != len(_option): # Can't use the same letter twice
            _error("socket already in use")
          _wiring = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
          for _index in range(0, len(_option), 2):
            _first, _second = _wiring.index(_option[_index]), _wiring.index(_option[_index + 1])
            _wiring[_first], _wiring[_second] =  _wiring[_second], _wiring[_first]
          _plugboard = Rotor(_wiring) # Update plug-board (steckerbrett) settings
      elif _arg in ["--rotors","-w"]:
        if (_count + 1) < len(sys.argv) and sys.argv[_count + 1][0] != "-": # Check argument given
          _count += 1
          _rotors = [] 
          _option = ''
          _next = ','
          while _count < len(sys.argv) and (_next == ','): # Read comma separated list of settings from the command line
            _option += sys.argv[_count].upper()
            _next = _option.strip()[-1:]
            _option = _option.replace(' ','') # Remove any spaces
            _count += 1
            if _next != ',' and _count < len(sys.argv): # Look ahead
              _next = sys.argv[_count].upper().strip()[-1:]
          _count -= 1
          for _name in _option.split(','):
            if _name in _rotor:
              _rotors.append(_rotor[_name])
            else:
              _error ("invalid rotor")
          _option = _option.split(',')
      elif _arg in ["--help", "-?"]:
        _about()
      elif _arg in "--version":
        _version()
      else:
        if _arg[:2] == "--":
          _error ("unrecognised option -- '" + (_arg + "'"))
        else:
          _error ("invalid option -- '" + (_arg[1:] + "'"))
    else:
      _text.append(_arg) # Just append the argument to the text if it isn't a command line option
    _count += 1

  enigma = Enigma(_plugboard, _selected, _rotors, _settings, _rings)

  _text = " ".join(_text)
  sys.stdout.write(_text + "\n")
  sys.stdout.write(enigma.encrypt(_text) + "\n")
  raise SystemExit 
