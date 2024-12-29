#!/usr/bin/python
#
#  py-enigma
#
#  An enigma machine simulator.
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
#   19 Dec 25   0.1   - Initial version - MT
#   25 Dec 25   0.2   - Added command line parsing (implemented without the 
#                       use of argparse or optargs to keep any dependencies
#                       to a minimum - MT
#                     - The text and initial rotor positions are now passed
#                       from the command line - MT
#                     - Improved verbose output - MT
#                     - Steps the next rotor after the position reaches the
#                       notch on the current rotor (need to fix the  double
#                       stepping behaviour of the M3 or M4) - MT
#   29 Dec 25   0.3   - Reduced the level of verbosity to a single level of
#                       detail (it is now all or nothing) - MT
#                     - Map the specified wiring of each rotor to the input
#                       and output paths using a lookup table, which allows
#                       the  ring position (Ringstellung) to be  configured
#                       when a rotor is initialised - MT
#                       
#   Requires:         - sys, os
#
#   To Do:            - Implement double stepping behaviour.
#

_VERSION = "0.3"

import sys, os

_verbose = 0
_wiring = 1

def _about():
  sys.stdout.write("Usage: " + sys.argv[0] + "[OPTION]... [FILE]...\n"
    "Decodes binary arguments.\n" + "\n" +
    "  -s, --setting (AAA)      initial rotor settings (defaults to AAA)\n" +
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
  def __init__(self, wiring, notch, ring):
    self.wiring = wiring
    self.notch = notch
    self.ring = ring
    self.position = 0
    self.inp = [None] * 26
    self.out = [None] * 26
    for _count, _char in enumerate(self.wiring):
      self.inp[_count] = ord(_char) - 65
    for _count, _value in enumerate(self.inp):
      self.out[_value] = _count

  def forward(self, char):
    _shift = (ord(char) - 65 + self.position - self.ring ) % 26
    _output = self.inp[_shift]
    if _verbose > 0: sys.stdout.write(chr((ord(char) - 65 + self.position) % 26 + 65) + "->" + chr(_output + self.ring + 65) + "; ")
    return chr((_output + 26 - self.position + self.ring) % 26 + 65)

  def backward(self, char):
    _shift = (ord(char) - 65 + self.position - self.ring ) % 26
    _output = self.out[_shift]
    if _verbose > 0: sys.stdout.write(chr((ord(char) - 65 + self.position) % 26 + 65) + "->" + chr(_output + self.ring + 65) + "; ")
    return chr((_output + 26 - self.position + self.ring) % 26 + 65)

  def rotate(self):
    self.position = (self.position + 1) % 26
    return (self.position - 1) == (ord(self.notch) - 65) # Return true if position matched notch

class Enigma:
  def __init__(self, rotors, reflector, rotor_positions):
    self.rotors = rotors
    self.reflector = reflector
    self.reset(rotor_positions)

  def reset(self,rotor_positions):
    for rotor, position in zip(self.rotors, reversed(rotor_positions)):
      rotor.position = ord(position) - 65

  def encrypt(self, message):
    result = ""
    for char in message.upper():
      if char.isalpha():
        self.rotate_rotors()
        if _verbose > 0: 
          for rotor in reversed(self.rotors):
            sys.stdout.write(chr(rotor.position + 65))
          sys.stdout.write(" " + char + " ")
        for rotor in self.rotors:
          char = rotor.forward(char)
        char = self.reflector.forward(char)
        for rotor in reversed(self.rotors):
          char = rotor.backward(char)
        if _verbose > 0: sys.stdout.write(char + "\n")
        result += char
      else:
        result += char
    return result

  def rotate_rotors(self):
    _rotate = True # Always moves the first rotor.
    for rotor in self.rotors:
      if _rotate: 
        _rotate = rotor.rotate()


_text = []
_state = "AAA"
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
        _state = sys.argv [_count].upper()
        if not(_state.isalpha() and len(_state)) == 3:
          _error("invalid rotor setting")
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

right =     Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q', 0)        # Rotor 'I'
middle =    Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E', 0)        # Rotor 'II'
left =      Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V', 0)        # Rotor 'III'
reflector = Rotor("YRUHQSLDPXNGOKMIEBFZCWVJAT", ' ', 0)        # Reflector 'B'
enigma =    Enigma([right, middle, left], reflector, _state)

_text = " ".join(_text)
sys.stdout.write(enigma.encrypt(_text) + "\n")
raise SystemExit 
