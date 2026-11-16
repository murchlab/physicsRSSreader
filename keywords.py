# from authorFormatFunction import myAuthorFormat

#List of keywords and key-authors for selecting papers to include in summary.

# Keyword matching (see myFormat in functionDefs.py) is case- and accent-insensitive, treats hyphens and
# other punctuation as spaces, and matches whole words (a trailing plural "s"/"es" is allowed):
#   "transmon" -> "transmons", "Transmon";  "neutral atom" does NOT match "neutral atomic oxygen".
# End a keyword with * to match any word starting with it:
#   "error correct*" -> "error correction", "error-correcting";  "fault toleran*" -> "fault-tolerant", "fault tolerance"

# Specific terms: a match in the title OR the abstract counts.
keywords = [
    ######## Superconducting circuits / cQED
    "Josephson",
    "Paramp",
    "JPA",
    "JPC",
    "TWPA",
    "traveling wave parametric",
    "travelling wave parametric",
    "quantum limited",
    "quantum limit",
    "phase preserving",
    "phase sensitive amplif*",
    "squeezing",
    "squeezed",
    "transmon",
    "fluxonium",
    "gatemon",
    "flux qubit",
    "superconducting qubit",
    "superconducting circuit",
    "superconducting resonator",
    "superconducting quantum processor",
    "superconducting processor",
    "circuit quantum electrodynamics",
    "circuit QED",
    "cQED",
    "microwave loss",
    "two level system",
    "quasiparticle",
    "kinetic inductance",
    "dispersive readout",
    "qubit readout",
    "measurement induced",
    "quantum nondemolition",
    "quantum non demolition",
    "weak measurement",
    "quantum trajector*",
    "quantum feedback",
    "Kerr cat",
    "cat qubit",
    "dual rail",
    "microwave to optical",
    "quantum transduc*",

    ######## Error correction / fault tolerance
    "error correct*",
    "error correcting code",
    "logical qubit",
    "logical error",
    "logical gate",
    "logical operation",
    "surface code",
    "color code",
    "colour code",
    "toric code",
    "stabilizer code",
    "stabilizer measurement",
    "syndrome extraction",
    "syndrome measurement",
    "LDPC",
    "qLDPC",
    "bivariate bicycle",
    "bosonic code",
    "GKP",
    "Gottesman Kitaev Preskill",
    "cat code",
    "binomial code",
    "magic state",
    "lattice surgery",
    "erasure qubit",
    "erasure conversion",
    "erasure error",
    "biased noise",
    "noise bias",
    "leakage reduction",
    "below threshold error",
    "below the surface code threshold",
    "error mitigation",

    ######## Electrons on neon / helium
    "electron on neon",
    "electrons on neon",
    "electron on solid neon",
    "electrons on solid neon",
    "solid neon",
    "electron on helium",
    "electrons on helium",
    "electron on liquid helium",
    "electrons on liquid helium",
    "electron on superfluid helium",
    "electrons on superfluid helium",
    "eNe qubit",
    "eHe qubit",

    ######## Neutral atoms
    "Rydberg",
    "neutral atom",
    "tweezer array",
    "atom array",
    "atomic array",
    "quantum gas microscop*",

    ######## Trapped ions
    "trapped ion",
    "ion trap",
    "Penning trap",
    "ion crystal",
    "ion chain",
    "QCCD",
    "quantum charge coupled",

    ######## Spin qubits / quantum dots / spin defects
    "spin qubit",
    "hole spin",
    "double quantum dot",
    "quantum dot array",
    "singlet triplet",
    "SiGe",
    "silicon qubit",
    "germanium qubit",
]

# Broader terms: only count when they appear in the TITLE (in abstracts they'd match too much).
titleOnlyKeywords = [
    "qubit",
    "Parametric",
    "quantum circuit",
    "quantum electrodynamics",
    "coherence time",
    "quantum dot",
    "optical lattice",
    "bosonic qubit",
    "bosonic mode",
    "decoder",
    "decoding",
    "quantum feedback",
    "fault toleran*",
    "optical tweezer",
    "quantum memor*",
    "nitrogen vacancy",
    "NV center",
    "NV centre",
    "random walk",
    "quantum machine learning",
    "boltzmann machine",
]

titlelist = keywords + titleOnlyKeywords   # searched in titles
wordlist = keywords                        # searched in abstracts

# Authors whose papers go in the "PROBABLY OF INTEREST" section.
# Matching uses only first initial + last name, case- and accent-insensitive
# ("Michel H. Devoret" == "M. Devoret" == "michel devoret"), so middle names don't matter.
# Names that collapse to a very common initial+surname (e.g. "J. Kim", "Y. Wang") would flood the
# digest with false positives; those are kept commented out at the bottom -- enable at your own risk.
authors = [
    ######## Superconducting circuits -- experiment, North America
    "Irfan Siddiqi",
    "John Clarke",
    "Alp Sipahigil",
    "Michel Devoret",
    "Robert Schoelkopf",
    "Michael Hatridge",
    "Peter Rakich",
    "Yiwen Chu",
    "John Martinis",
    "David Schuster",
    "Andrew Houck",
    "Nathalie de Leon",
    "Jeff Thompson",
    "William Oliver",
    "Kevin O'Brien",
    "Mollie Schwartz",
    "Kyle Serniak",
    "Kater Murch",
    "Jose Aumentado",
    "Joe Aumentado",
    "John Teufel",
    "Raymond Simmonds",
    "Konrad Lehnert",
    "Cindy Regal",
    "Andrew Cleland",
    "Aaron Chou",
    "Srivatsan Chakram",
    "Robert McDermott",
    "Britton Plourde",
    "Matthew LaHaye",
    "Eli Levenson-Falk",
    "Machiel Blok",
    "Shyam Shankar",
    "Alicia Kollar",
    "Oskar Painter",
    "Mohammad Mirhosseini",
    "Amir Safavi-Naeini",
    "Jonathan Simon",
    "Adrian Lupascu",
    "Christopher Wilson",
    "Max Hofheinz",
    "Benjamin Palmer",
    "Andrew Higginbotham",

    ######## Superconducting circuits -- industry labs
    "Jay Gambetta",
    "Jerry Chow",
    "Oliver Dial",
    "Antonio Corcoles",
    "Zlatko Minev",
    "Andrew Eddins",
    "Hartmut Neven",
    "Julian Kelly",
    "Pedram Roushan",
    "Daniel Sank",
    "Charles Neill",
    "Sergio Boixo",
    "Kostyantyn Kechedzhi",
    "Alexis Morvan",

    ######## Superconducting circuits -- experiment, Europe
    "Andreas Wallraff",
    "Christopher Eichler",
    "Leonardo DiCarlo",
    "Gary Steele",
    "Benjamin Huard",
    "Audrey Bienfait",
    "Nicolas Roch",
    "Olivier Buisson",
    "Patrice Bertet",
    "Emmanuel Flurin",
    "Landry Bretheau",
    "Zaki Leghtas",
    "Philippe Campagne-Ibarcq",
    "Raphael Lescanne",
    "Ioan Pop",
    "Alexey Ustinov",
    "Gerhard Kirchmair",
    "Johannes Fink",
    "Per Delsing",
    "Simone Gasparinetti",
    "Jonas Bylander",
    "Giovanna Tancredi",
    "Mikko Mottonen",
    "Jukka Pekola",
    "Stefan Filipp",
    "Rudolf Gross",
    "Peter Leek",
    "Morten Kjaergaard",
    "Pasquale Scarlino",
    "Vladimir Manucharyan",
    "Tobias Kippenberg",
    "Shay Hacohen-Gourgy",

    ######## Superconducting circuits -- experiment, Asia / Australia
    "Yasunobu Nakamura",
    "Kouichi Semba",

    ######## Electrons on neon / helium
    "Dafei Jin",
    "Denis Konstantinov",
    "Erika Kawakami",
    "Johannes Pollanen",
    "Stephen Lyon",
    "Gerwin Koolstra",
    "Niyaz Beysengulov",
    "Kyle Castoria",
    "Mark Dykman",
    "Maja Cassidy",

    ######## Neutral atoms
    "Mikhail Lukin",
    "Markus Greiner",
    "Vladan Vuletic",
    "Wolfgang Ketterle",
    "Giulia Semeghini",
    "Dolev Bluvstein",
    "Manuel Endres",
    "Hannes Bernien",
    "Cheng Chin",
    "Waseem Bakr",
    "Adam Kaufman",
    "Mark Saffman",
    "Jacob Covey",
    "Shimon Kolkowitz",
    "Dan Stamper-Kurn",
    "Antoine Browaeys",
    "Thierry Lahaye",
    "Immanuel Bloch",
    "Johannes Zeiher",
    "Monika Aidelsburger",
    "Selim Jochim",
    "Matthias Weidemuller",
    "Tilman Esslinger",
    "Philipp Treutlein",
    "Charles Adams",
    "Stefan Kuhr",
    "Shannon Whitlock",

    ######## Trapped ions
    "Christopher Monroe",
    "Kenneth Brown",
    "Norbert Linke",
    "Crystal Noel",
    "David Wineland",
    "Dietrich Leibfried",
    "Daniel Slichter",
    "John Bollinger",
    "John Chiaverini",
    "Isaac Chuang",
    "Hartmut Haffner",
    "Wesley Campbell",
    "Eric Hudson",
    "Rainer Blatt",
    "Thomas Monz",
    "Christian Roos",
    "Tracy Northup",
    "Ben Lanyon",
    "Jonathan Home",
    "David Lucas",
    "Winfried Hensinger",
    "Ferdinand Schmidt-Kaler",
    "Piet Schmidt",
    "Christian Ospelkaus",
    "Roee Ozeri",
    "Dzmitry Matsukevich",

    ######## Spin qubits / quantum dots / spin defects
    "Lieven Vandersypen",
    "Menno Veldhorst",
    "Giordano Scappucci",
    "Anasua Chatterjee",
    "Ronald Hanson",
    "Tim Taminiau",
    "Jason Petta",
    "Mark Eriksson",
    "John Nichol",
    "Thaddeus Ladd",
    "Amir Yacoby",
    "David Awschalom",
    "Ania Jayich",
    "Ferdinand Kuemmeth",
    "Dominik Zumbuhl",
    "Hendrik Bluhm",
    "Lars Schreiber",
    "Silvano De Franceschi",
    "Tristan Meunier",
    "Natalia Ares",
    "Floris Zwanenburg",
    "Andrea Morello",
    "Andrew Dzurak",
    "Michelle Simmons",
    "Arne Laucht",
    "Seigo Tarucha",

    ######## Theory
    "K. Birgitta Whaley",
    "Ehud Altman",
    "Steven Girvin",
    "Shruti Puri",
    "Aashish Clerk",
    "Jens Koch",
    "Archana Kamal",
    "Hakan Tureci",
    "Alexandre Blais",
    "Alexander Korotkov",
    "Justin Dressel",
    "Andrew Jordan",
    "Andrew Baker",
    "John Preskill",
    "Daniel Gottesman",
    "Austin Fowler",
    "Craig Gidney",
    "Nicolas Delfosse",
    "Mohammad Hafezi",
    "Alexey Gorshkov",
    "Ana Maria Rey",
    "Susan Coppersmith",
    "Mark Friesen",
    "Barbara Terhal",
    "Mazyar Mirrahimi",
    "Frank Wilhelm",
    "David DiVincenzo",
    "Peter Rabl",
    "Goran Johansson",
    "Klaus Molmer",
    "Anders Sorensen",
    "Peter Zoller",
    "Hannes Pichler",
    "Ignacio Cirac",
    "Jens Eisert",
    "Earl Campbell",
    "Daniel Loss",
    "Guido Burkard",
]

# Common initial+surname collisions -- uncomment to enable (expect some unrelated papers):
#   "Jian-Wei Pan",   # -> "j pan"
#   "Jun Ye",         # -> "j ye"
#   "Liang Jiang",    # -> "l jiang"
#   "Luyan Sun",      # -> "l sun"
#   "Chen Wang",      # -> "c wang"
#   "Jungsang Kim",   # -> "j kim"
#   "Kihwan Kim",     # -> "k kim"
#   "Christian Andersen", # -> "c andersen"  (very common Danish surname)
#   "Andrew Wilson",  # -> "a wilson"
#   "Xuedong Hu",     # -> "x hu"
#   "Xiaobo Zhu",     # -> "x zhu"
#   "Alexander Ma",   # -> "a ma"
#   "Norman Yao",     # -> "n yao"
#   "Kang-Kuen Ni",   # -> "k ni"
#   "Hong Tang",      # -> "h tang"
#   "Wei Guo",        # -> "w guo"   (electrons on helium/neon, FSU)
#   "Ge Yang",        # -> "g yang"  (electrons on helium)
#   "Xianjing Zhou",  # -> "x zhou"  (electron-on-neon qubit)
#   "Jaw-Shen Tsai",  # -> "j tsai"


# authors = [myAuthorFormat(author) for author in authors]

#def generateInitialsCombinationsMultiple(authorList):
#    temp=[generateInitialsCombinations(author) for author in authorList]
#    #the next line is flattening "temp"
#    return([item for sublist in temp for item in sublist])
#
#def generateInitialsCombinations(author):
#    combos=[]
#    names=author.split(" ")
#    if len(names) == 1:
#        return([author])
#
#    #First name:
#    if len(names[0].strip('.')) > 1: #if first name listed is not just an initial
#        combos.append(names[0][0]+'.') #add possibility of having only initial for first name to combo list
#    combos.append(names[0])
#
#    #Later names, but not last name:
#    for name in names[1:-1]:
#        if len(name.strip('.')) > 1: #if name listed is not just an initial
#            combos = [[combo+' '+name,combo+' '+name[0]+'.',combo] for combo in combos]
#        else:
#            combos = [[combo+' '+name,combo] for combo in combos]
#        combos = [item for sublist in combos for item in sublist] #keeping list of combos flat
#
#    #Last name
#    lastName=names[-1]
#    combos = [combo+' '+lastName for combo in combos]
#    return(combos)
#
#authors = generateInitialsCombinationsMultiple(authors)

# Make case insensitive:
titlelist = [word.lower() for word in titlelist]
wordlist = [word.lower() for word in wordlist]
authors = [author.lower() for author in authors]
