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
#                       the  ring position (Ringstellung) to be  configured
#                       when a rotor is initialised - MT
#   30 Dec 24         - Added  a plug board (steckerbrett) by using a rotor
#                       to exchange pairs of letters - MT
#                     - The initial ring positions can now be specified  on 
#                       the command line - MT
#                     - Added a name property to the rotor class - MT
#                     - Fixed wheel stepping - MT
#                     - Rotors  can have multiple turnover positions  which 
#                       allows the use of rotors VI VII and VIII - MT
#                     - Fixed small bug in verbose output - MT
#
#   To Do:            - Allow  plug board settings to be specified  on  the 
#                       command line.
#

_VERSION = "0.4"

import sys, os

_verbose = 0
_wiring = 1

def _about():
  sys.stdout.write("Usage: " + sys.argv[0] + "[OPTION]... [FILE]...\n"
    "Decodes binary arguments.\n" + "\n" +
    "  -r, --rings (AAA)        set the initial ring positions (defaults to AAA)\n" +
    "  -s, --setting (AAA)      set the initial rotor positions (defaults to AAA)\n" +
    "  -v, --verbose            verbose output\n" +
    "  -?, --help               display this help and exit\n" +
    "      --version            output version information and exit\n\n" +
    "Example:\n" +
    "  " + os.path.basename(sys.argv[0]) + " -s OKW ENIGMA\n")
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
  def __init__(self, name = '', wiring = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", turnover = None):
    self.name = name
    self.wiring = wiring
    self.ring = 0
    self.position = 0
    self.turnover = [False] * 26
    if turnover is not None and turnover.isalpha(): 
      for _char in turnover.upper():
        self.turnover[ord(_char.upper()) - 65] = True
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
    self.position = (self.position + 1) % 26 # Move rotor by one step.  
    return _rotate # Return true if position matched notch


class Enigma:
  def __init__(self, plugboard, rotors, reflector, state, rings):
    self.plugboard = plugboard
    self.rotors = rotors
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


_text = []
_settings = "AAA"
_rings = "AAA"
_verbose = 0
_count = 1

while _count < len(sys.argv):
  _arg = sys.argv [_count]
  if _arg[:1] == "-" and len(_arg) > 1:
    if _arg in ["--verbose", "-v"]:
      _verbose += 1
    elif _arg in ["--setting","-s"]:
      _count += 1
      if _count < len(sys.argv):
        _settings = sys.argv [_count].upper()
        if not(_settings.isalpha() and len(_settings) == 3):
          _error("invalid rotor setting")
    elif _arg in ["--ring","-r"]:
      _count += 1
      if _count < len(sys.argv):
        _rings = sys.argv [_count].upper()
        if not(_rings.isalpha() and len(_rings) == 3):
          _error("invalid ring setting")
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
    _text.append(_arg) # If it isn't a qualified
  _count += 1


rotor_I =     Rotor("I",    "EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')
rotor_II =    Rotor("II",   "AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')
rotor_III =   Rotor("III",  "BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')
rotor_IV =    Rotor("IV",   "ESOVPZJAYQUIRHXLNFTGKDCMWB", 'J')
rotor_V =     Rotor("V",    "VZBRGITYUPSDNHLXAWMJQOFECK", 'Z')
rotor_VI =    Rotor("VI",   "JPGVOUMFYQBENHZRDKASXLICTW", 'zm')
rotor_VII =   Rotor("VII",  "NZJHGRCXMYSWBOUFAIVLPEKQDT", 'ZM')
rotor_VIII =  Rotor("VIII", "FKQHTLXOCBJSPDZRAMEWNIUYGV", 'ZM')
rotor_B =     Rotor("B",    "YRUHQSLDPXNGOKMIEBFZCWVJAT", None) # Reflector 'B'

plugboard =   Rotor() # Empty plugboard (steckerbrett)

left =      rotor_III
middle =    rotor_II
right =     rotor_I
reflector = rotor_B

enigma = Enigma(plugboard,[right, middle, left], reflector, _settings, _rings)

_text = " ".join(_text)
sys.stdout.write(_text + "\n" + enigma.encrypt(_text) + "\n")
raise SystemExit 
