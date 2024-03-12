# from authorFormatFunction import myAuthorFormat

#List of keywords and key-authors for selecting papers to include in summary.

#title list
titlelist = ["Josephson",
             "Parametric",
             "Paramp",
             "JPA",
             "JPC",
             "qubit",
             "squeezing",
             "squeezed"
             "quantum limit",
             "quantum limited",
             "phase preserving",
             "phase sensitive",
             "quantum feedback",
             "coherence times",
             "random walk",
             "quantum machine learning",
             "boltzmann machine",
             "transmon",
             "fluxonium",
             "microwave loss",
             "quasiparticle",
             "quantum electrodynamics",
             "superconducting circuit",
             "quantum circuit",
             "superconducting resonator"
             ]

#This is the word list we will care about for abstracts
wordlist = titlelist #[]
#Here one inputs the authors...make sure the capitalization is correct (also beware of weird symbols in name)
#TODO: so far only 1 author appears in the print file.  Need a fix for multiple authors of interest on one entry.  Also, if you want to make sure you get the author right...you can copy his/her URL
authors = [
            #####Experimental PI's
            "Irfan Siddiqi",
            "Michel Devoret",
            "Robert J. Schoelkopf",
            "John Clarke",
            "John Martinis", 
            "David Schuster",
            "William D. Oliver",
            "Andrew A. Houck",
            "Kater W. Murch",
            "Rajamani Vijay",
            "Rajamani Vijayaraghavan",
            "Nicolas Roch",
            "Benjamin Huard",
            "Jose Aumentado",
            "Joe Aumentado",
            "John D. Teufel",
            "Andreas Wallraff",

            ######Theory PI's
            "Aashish A. Clerk",
            "Alexandre Blais",
            "Andrew Baker",
            "K. Birgitta Whaley",
            "Alexander N. Korotkov",
            "Justin Dressel",

            ######Smattering of post-docs and grad-students

            #QNL related
            "Christopher Macklin",
            "Steven Weber",
            "Mollie Schwartz",
            "Mollie E. Schwartz",
            "Mollie Kimchi-Schwartz",
            "Vinay V. Ramasesh",
            "Leigh Martin",
            "Shay Gourgy",
            "Shay Hacohen-Gourgy",
            "Allison Dove",
            "David M. Toyli",
            "Eli M. Levenson-Falk",
            "Daniel Slichter",
            "Annirudh Narla",
            "Zlatko Minev",
            "Aditya Venkataraman",
            "Aditya Venkatramani",
            "Nicholas Frattini",
            "Emmanuel Flurin",
            "Andrew W. Eddins",
            "William P. Livingston",
            "John Mark Kreikebaum",
            "James Colless",
            "Machiel Blok",
            "Sydney Schreppler",
            "Kevin O'Brien",


            "Landry Bretheau",

            "Daniel Sank"
           ]


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
titlelist = map(str.lower,titlelist)
wordlist = map(str.lower,wordlist)
authors = map(str.lower,authors)
