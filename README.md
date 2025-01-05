# gcc-enigma

An implementation of an engima simulator written in C.

Work in progress

## Enigma M1, M3 and M4

### Rotors

The standard wiring for each of the different rotors is shown below:

The M1 enigma machines were provided with could use three of five  possible
rotors (I-V), with three additional rotors being available for use with the
later M3 (VI, VII and VIII).  

For  added complexity the M4 used a thinner reflector which allowed another
thinner  rotor to be added.  This 4th rotor was one of two thin rotors used
(either Beta and Gamma).  Note that once the initial position had been  set
the fourth rotor remained fixed.

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

Three  different  reflectors could be used with the M3 with  two  different
reflectors being used with the Mk4 as shown below:

```
Reflector ABCDEFGHIJKLMNOPQRSTUVWXYZ  Notch           Turnover

M3
   UKW-A  EJMZALYXVBWFCRQUONTSPIKHGD                    Fixed
   UKW-B  YRUHQSLDPXNGOKMIEBFZCWVJAT                    Fixed
   UKW-C  FVPJIAOYEDRZXWGCTKUQSBNMHL                    Fixed
```

```
M4
   UKW-B  ENKQAUYWJICOPBLMDXZVFTHRGS                    Fixed
   UKW-C  RDOBJNTKVEHMLFCWZAXGYIPSUQ                    Fixed
```

## Enigma Model G

The machine in the Bletchley Park Museum on loan from GCHQ has a  different
design  to the others and unlike the M1, M3 and M4 it uses a series of cogs 
and pinion wheels to advance the rotors and so does not exhibit the  double
stepping behaviour of the M1, M3 and M4.

There are several other notable diffeences.

- There is no plug-board.
- The number of notches is increased.  
- The reflector is not fixed but steps like the other rotors.
- The wiring of every rotor includign the entry wheel is different.

The  table  below shows the wiring of the rotors used by the German  Abwehr
(military intelligence service).
```
Rotor     ABCDEFGHIJKLMNOPQRSTUVWXYZ  Notch             Turnover

   ETW    QWERTZUIOASDFGHJKPYXCVBNML                    Fixed

   I      DMTWSILRUYQNKFEJCAZBPGXOHV  ACDEHIJKMNOQSTWXY SUVWZABCEFGIKLOPQ
   II     HQZGPJTMOBLNCIFDYAWVEUSRKX  ABDGHIKLNOPSUVY   STVYZACDFGHKMNQ
   III    UQNTLSZFMREHDPXKIBVYGJCWOA  CEFIMNPSUVZ       UWXAEFHKMNR

   UKW    RULQMZJSYGOCETKWDAHNBXPVIF                    
```

## Examples

Encipher a message using the default settings.

```
$ ./py-enigma.py the quick brown fox jumped over the lazy dog
ZPT RRATE UJDAW KFJ ABUUQN UMTW BMC TEGL HQA
```

Decipher a message using a different rotor setting.

```
$ ./py-enigma.py -s two qvt peahy ekwva lgj dtovdt bzkd ayu ruxk kxf
THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG
```

Select the rotors to be used.

```
$ ./py-enigma.py -w III, II, I -s two qvt peahy ekwva lgj dtovdt bzkd ayu ruxk kxf
THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG
```

To decipher the last message sent from the battleship Scharnhorst you  need
to select the rotors used, configure the matching ring settings and initial 
rotor positions then set up the plug-board using the following command.

```
$ ./py-enigma.py -w III, VI, VIII -r AHM -s UZV -p AN,EZ,HK,IJ,LR,MQ,OT,PV,SW,UX YKAE NZAP MSCH ZBFO CUVM RMDP YCOF HADZ IZME FXTH FLOL PZLF GGBO TGOX GRET DWTJ IQHL MXVJ WKZU ASTR
YKAE NZAP MSCH ZBFO CUVM RMDP YCOF HADZ IZME FXTH FLOL PZLF GGBO TGOX GRET DWTJ IQHL MXVJ WKZU ASTR
STEU EREJ TANA FJOR DJAN STAN DORT QUAA ACCC VIER NEUN NEUN ZWOF AHRT ZWON ULSM XXSC HARN HORS THCO

steuere j tanafjord j an standort qu aaa ccc vier neun neun zwo fahrt zwo nul sm xx scharnhorst hco

```

### Links

https://en.wikipedia.org/wiki/Enigma_machine

https://en.wikipedia.org/wiki/Enigma_rotor_details

https://www.cryptomuseum.com/crypto/enigma/

https://cryptocellar.org/bgac/scharnhorst.html

https://piotte13.github.io/enigma-cipher/

