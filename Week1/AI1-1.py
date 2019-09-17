node = 'FGCW|'

def is_goal(node):
    if(node == '|FGCW'):
        return True

def check_side(currentSide,destSide):
    if "F" in currentSide:
        for letter in currentSide:
            currentSide.replace("F", "")
            currentSide = "".join(sorted(currentSide))
            destSide += "F"
            destSide = "".join(sorted(destSide))

            currentSide.replace(letter, "")
            currentSide = "".join(sorted(currentSide))
            destSide += letter
            destSide = "".join(sorted(destSide))

            res = currentSide + "|" + destSide
            print(res)



def succesors(node):
    riverSides = node.split("|")
    left = riverSides[0]
    right = riverSides[1]
    check_side(left,right)


    split = node.split("|")
    validOptions = []

    for option in split:
        invalidLetter = ""
        for letter in option:
            if letter == invalidLetter:
                break
            if letter == "F":
                break
            elif letter == "G":
                invalidLetter = "W"
            elif letter == "C":
                invalidLetter = "G"
            elif letter == "W":
                invalidLetter = "G"
        validOptions.append(option)










def find_all_paths(node, path=[]):
    path = path + [node] # voeg een node toe aan de path array

    if is_goal(node):
        return [path]

    paths = []  # a list of all paths

    for child in succesors(node):
        if child not in path:
            # return list of paths from here
            newpaths = find_all_paths(child, path)
            # add every path found to paths
            for newpath in newpaths:
                paths.append(newpath)

    return paths

print(find_all_paths(node))
