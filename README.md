## gcc-enigma

An implementation of an engima simulator written in C.

** Work in progress **

### Rotors

The standard wiring for each of the different rotors is shown below:

The Mk1 enigma machines could use three of five possible rotors (I-V), with
three additional possible rotors being available for use with the later Mk3 
(VI, VII and VIII).  

For added complexity the Mk4 used a thinner reflector which allowed another 
thinner rotors to be added.  This 4th rotor was one of two additional  thin
rotors (Beta and Gamma) available.  Note that the 4th rotor was not rotated
once the initial rotor position had been set.

Compatibility between the Mk4 machines and the Mk3 is maintained by setting
the 4th rotor to the 'A' position.
```
  Rotor   ABCDEFGHIJKLMNOPQRSTUVWXYZ  Notch           Turnover

   ETW    ABCDEFGHIJKLMNOPQRSTUVWXYZ                   Fixed

   I      EKMFLGDQVZNTOWYHXUSPAIBRCJ    Y                Q
   II     AJDKSIRUXBLHWTMCQGZNPYFVOE    M                E
   III    BDFHJLCPRTXVZNYEIWGAKMUSQO    D                V
   IV     ESOVPZJAYQUIRHXLNFTGKDCMWB    R                J
   V      VZBRGITYUPSDNHLXAWMJQOFECK    H                Z

   VI     JPGVOUMFYQBENHZRDKASXLICTW    HU               ZM
   VII    NZJHGRCXMYSWBOUFAIVLPEKQDT    HU               ZM
   VIII   FKQHTLXOCBJSPDZRAMEWNIUYGV    HU               ZM

   Beta   LEYJVCNIXWPBQMDRTAKZGFUHOS                   Fixed
   Gamma  FSOKANUERHMBTIYCWLQPZXVGJD                   Fixed
```


### Reflectors

Three different reflectors could be used as shown below:
```
Reflector ABCDEFGHIJKLMNOPQRSTUVWXYZ  Notch           Turnover

Mk3
   UKW-A  EJMZALYXVBWFCRQUONTSPIKHGD
   UKW-B  YRUHQSLDPXNGOKMIEBFZCWVJAT
   UKW-C  FVPJIAOYEDRZXWGCTKUQSBNMHL

Mk4
   UKW-B  ENKQAUYWJICOPBLMDXZVFTHRGS 
   UKW-C  RDOBJNTKVEHMLFCWZAXGYIPSUQ
```
The machine in the Bletchley Park Museum on loan from GCHQ is a different
model with a different rotor arrangement.  As well as the wiring of every
rotor being different the number of notches is increased (17 on the first
15 on the second and 11 on the third).
```
Rotor     ABCDEFGHIJKLMNOPQRSTUVWXYZ  Notch             Turnover

Entry     QWERTZUIOASDFGHJKPYXCVBNML                    Fixed

  I       DMTWSILRUYQNKFEJCAZBPGXOHV  ACDEHIJKMNOQSTWXY SUVWZABCEFGIKLOPQ
  II      HQZGPJTMOBLNCIFDYAWVEUSRKX  ABDGHIKLNOPSUVY   STVYZACDFGHKMNQ
  III     UQNTLSZFMREHDPXKIBVYGJCWOA  CEFIMNPSUVZ       UWXAEFHKMNR

Reflector RULQMZJSYGOCETKWDAHNBXPVIF                    
```


### Example

```
$ ./py-enigma.py the quick brown fox jumped over the lazy dog
ZPT RRATE UJDAW KFJ ABUUQN UMTW BMC TEGL HQA
```
```
$ ./py-enigma.py --setting two qvt peahy ekwva lgj dtovdt bzkd ayu ruxk kxf
THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG
```

### Links

https://www.cryptomuseum.com/crypto/enigma/

