#!/usr/bin/python
#
#  py-enigma
#
#  An enigma machine simulator.
#
#  This  program is free software: you can redistribute it and/or modify  it
#  under  the  terms of the GNU General Public License as published  by  the
#  Free  Software  Foundation, either version 3 of the License, or (at  your
#  option) any later version.
#
#  This  program  is  distributed in the hope that it will  be  useful,  but
#  WITHOUT   ANY   WARRANTY;   without  even   the   implied   warranty   of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
#  Public License for more details.
#
#  You  should have received a copy of the GNU General Public License  along
#  with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  19 Dec 25   0.1   - Initial version - MT
#

_VERSION = "0.1"

import sys

class Rotor:
  def __init__(self, wiring, notch):
    self.wiring = wiring
    self.notch = notch
    self.position = 0

  def forward(self, char):
    shift = (ord(char) - 65 + self.position) % 26
    return chr((ord(self.wiring[shift]) - 65 - self.position) % 26 + 65)

  def backward(self, char):
    shift = (ord(char) - 65 + self.position) % 26
    return chr((self.wiring.index(chr(shift + 65)) - self.position) % 26 + 65)

  def rotate(self):
    self.position = (self.position + 1) % 26
    return self.position == self.notch

class Reflector:
  def __init__(self, wiring):
    self.wiring = wiring

  def reflect(self, char):
    return self.wiring[ord(char) - 65]

class EnigmaMachine:
  def __init__(self, rotors, reflector, rotor_positions):
    self.rotors = rotors
    self.reflector = reflector
    for rotor, position in zip(self.rotors, rotor_positions):
        rotor.position = ord(position) - 65

  def reset(self, rotors, reflector, rotor_positions):
    self.rotors = rotors
    self.reflector = reflector
    for rotor, position in zip(self.rotors, rotor_positions):
      rotor.position = ord(position) - 65

  def encrypt(self, message):
    result = ""
    for char in message.upper():
      if char.isalpha():
        self.rotate_rotors()
        for rotor in self.rotors:
          char = rotor.forward(char)
        char = self.reflector.reflect(char)
        for rotor in reversed(self.rotors):
          char = rotor.backward(char)
        result += char
      else:
        result += char
    return result

  def rotate_rotors(self):
    if self.rotors[1].rotate():
      self.rotors[0].rotate()
    if self.rotors[2].rotate():
      self.rotors[1].rotate()

# Example usage
rotor1 = Rotor("EKMFLGDQVZNTOWYHXUSPAIBRCJ", 'Q')   # Rotor 'I'
rotor2 = Rotor("AJDKSIRUXBLHWTMCQGZNPYFVOE", 'E')   # Rotor 'II'
rotor3 = Rotor("BDFHJLCPRTXVZNYEIWGAKMUSQO", 'V')   # Rotor 'III'
reflector = Reflector("YRUHQSLDPXNGOKMIEBFZCWVJAT") # Reflector 'B'

enigma = EnigmaMachine([rotor1, rotor2, rotor3], reflector, "AAA")
plaintext = "HELLO WORLD\n"
sys.stdout.write(plaintext)
ciphertext = enigma.encrypt(plaintext) 
sys.stdout.write(ciphertext)
enigma = EnigmaMachine([rotor1, rotor2, rotor3], reflector, "AAA")
plaintext = enigma.encrypt(ciphertext)
sys.stdout.write(plaintext)
 
