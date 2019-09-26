#node = 'FGCW|'
node = {'F': 0, "G": 0, "C": 0, "W": 0}

def is_goal(node):
    if(parse_node(node) == '|FGCW'):
        return True

#Parse a node to the string
def parse_node(node):
    left = ''
    right = ''
    for key in node.keys():
        val = node[key]
        if val == 0:
            left += key
        else:
            right += key
    return left + "|" + right

def check_side(check_node):
    side_to_check = None
    if check_node["F"] == 0:
        side_to_check = 1
    else:
        side_to_check = 0
    side = []
    for key in check_node.keys():
        if check_node[key] == side_to_check:
            side.append(key)
    if "W" in side and "G" in side:
        return False

    if "G" in side and "C" in side:
        return False
    return True

def switch_side(node_copy,companion=None):
    if companion != None:
        if node_copy[companion] == 0: 
            node_copy[companion] = 1
        elif node_copy[companion] == 1:
            node_copy[companion] = 0
    if node_copy["F"] == 0:
        node_copy["F"] = 1
    elif node_copy["F"] == 1:
        node_copy["F"] = 0
    return [check_side(node_copy), node_copy]

def succesors(node):
    farmer_side = node['F']
    farmer_companions = [None]
    valid_options = []
    for key in node.keys():
        if key != "F":
            if node[key] == farmer_side:
                farmer_companions.append(key)
    for comp in farmer_companions:
        res = switch_side(node.copy(),comp)
        if res[0]:
            valid_options.append(res[1])

    return valid_options

def find_all_paths(node, path=[]):
    path = path + [parse_node(node)] # voeg een node toe aan de path array

    if is_goal(node):
        return [path]

    paths = []  # a list of all paths

    for child in succesors(node):
        if parse_node(child) not in path:
            # return list of paths from here
            newpaths = find_all_paths(child, path)
            # add every path found to paths
            for newpath in newpaths:
                paths.append(newpath)
    return paths
print(find_all_paths(node))
#O(b^d)
