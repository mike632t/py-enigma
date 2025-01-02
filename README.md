## gcc-enigma

An implementation of an engima simulator written in C.

Work in progress

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
   UKW-A  EJMZALYXVBWFCRQUONTSPIKHGD                    Fixed
   UKW-B  YRUHQSLDPXNGOKMIEBFZCWVJAT                    Fixed
   UKW-C  FVPJIAOYEDRZXWGCTKUQSBNMHL                    Fixed

Mk4
   UKW-B  ENKQAUYWJICOPBLMDXZVFTHRGS                    Fixed
   UKW-C  RDOBJNTKVEHMLFCWZAXGYIPSUQ                    Fixed
```

The machine in the Bletchley Park Museum on loan from GCHQ is a different
model with a different rotor arrangement.  As well as the wiring of every
rotor being different the number of notches is increased (17 on the first
15 on the second and 11 on the third).  This model also does NOT have the
double stepping behaviour of the Mk3 or Mk4 machines.

```
Rotor     ABCDEFGHIJKLMNOPQRSTUVWXYZ  Notch             Turnover

   ETW    QWERTZUIOASDFGHJKPYXCVBNML                    Fixed

   I      DMTWSILRUYQNKFEJCAZBPGXOHV  ACDEHIJKMNOQSTWXY SUVWZABCEFGIKLOPQ
   II     HQZGPJTMOBLNCIFDYAWVEUSRKX  ABDGHIKLNOPSUVY   STVYZACDFGHKMNQ
   III    UQNTLSZFMREHDPXKIBVYGJCWOA  CEFIMNPSUVZ       UWXAEFHKMNR

   UKW    RULQMZJSYGOCETKWDAHNBXPVIF                    
```

### Examples

Encoding using the default settings.

```
$ ./py-enigma.py the quick brown fox jumped over the lazy dog
ZPT RRATE UJDAW KFJ ABUUQN UMTW BMC TEGL HQA
```

Decode some text that was encoded using a different rotor setting.

```
$ ./py-enigma.py -s two qvt peahy ekwva lgj dtovdt bzkd ayu ruxk kxf
THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG
```

Currently  the only way to to use a different combination of rotors, or  to
configure the plugboard it to modify the code.

The following changes are therefore required to replicate the settings used
to encode the last message sent from the battlecruser Scharnhorst 

```
plugboard =   Rotor("    ", "NBCDZFGKJIHRQATVMLWOXPSUYE", ' ') # AN EZ HK IJ LR MQ OT PV SW and UX swapped
left = rotor_III
middle = rotor_VI
right = rotor_VIII
reflector = rotor_B
```

With these changes made the message can be decoded.

```
$ ./py-enigma.py -r AHM -s UZV YKAE NZAP MSCH ZBFO CUVM RMDP YCOF HADZ IZME FXTH FLOL PZLF GGBO TGOX GRET DWTJ IQHL MXVJ WKZU ASTR
YKAE NZAP MSCH ZBFO CUVM RMDP YCOF HADZ IZME FXTH FLOL PZLF GGBO TGOX GRET DWTJ IQHL MXVJ WKZU ASTR
STEU EREJ TANA FJOR DJAN STAN DORT QUAA ACCC VIER NEUN NEUN ZWOF AHRT ZWON ULSM XXSC HARN HORS THCO

steuere j tanafjord j an standort qu aaa ccc vier neun neun zwo fahrt zwo nul sm xx scharnhorst hco

```

### Links

https://www.cryptomuseum.com/crypto/enigma/

https://www.cryptomuseum.com/crypto/enigma/

https://en.wikipedia.org/wiki/Enigma_rotor_details

https://cryptocellar.org/bgac/scharnhorst.html

https://piotte13.github.io/enigma-cipher/

