from main import main

redTop = [[4],[1]]
redBottom = [[1],[0]]
blueTop = [[2],[2]]
blueBottom = [[0],[0]]
n = 3
polyString = main([redTop, redBottom], [blueTop, blueBottom], n)
polyStrings = polyString.split("Polynomial")
for polyString in polyStrings:
    terms = polyString.split("+")
    combos = {}
    for term in terms:
        powers = []
        if "x1" in term:
            if "x1^" in term:
                exp = ""
                i = term.find("x1^")
                while term[i] != "^":
                    i += 1
                i += 1
                while term[i] != " ":
                    exp += term[i]
                    i += 1
                powers.append(int(exp))
            else:
                powers.append(1)
        if "x2" in term:
            if "x2^" in term:
                exp = ""
                i = term.find("x2^")
                while term[i] != "^":
                    i += 1
                i += 1
                while term[i] != " ":
                    exp += term[i]
                    i += 1
                powers.append(int(exp))
            else:
                powers.append(1)
        if "x3" in term:
            if "x3^" in term:
                exp = ""
                i = term.find("x3^")
                while term[i] != "^":
                    i += 1
                i += 1
                while term[i] != " ":
                    exp += term[i]
                    i += 1
                powers.append(int(exp))
            else:
                powers.append(1)
        powers.sort()
        powers.reverse()
        distinct = len(set(powers))
        powerstring = str(powers)
        if powerstring in combos:
            match distinct:
                case 1:
                    match len(powers):
                        case 1:
                            combos[powerstring] += 1/3
                        case 2:
                            combos[powerstring] += 1/3
                        case 3:
                            combos[powerstring] += 1
                case 2:
                    match len(powers):
                        case 2:
                            combos[powerstring] += 1/6
                        case 3:
                            combos[powerstring] += 1/3
                case 3:
                    combos[powerstring] += 1/6
        else:
            match distinct:
                case 1:
                    combos[powerstring] = 1/3
                case 2:
                    combos[powerstring] = 1/3
                case 3:
                    combos[powerstring] = 1/6
    for k in combos:
        combos[k] = round(combos[k])
    outputstring = ""
    for k in combos:
        outputstring += "+"+str(combos[k])+"*m"+k
    outputstring = outputstring[1:]
    print(outputstring)
