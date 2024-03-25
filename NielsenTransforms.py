import sys

from generalClasses import Node
import networkx as nx
from pyvis.network import Network

variables = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
             'V', 'W','X', 'Y', 'Z','1', '2', '3', '4', '5', '6', '7', '8', '9', '0' ]
currentNodes = []
assignments = []
count = [1]
graph = nx.DiGraph()

def OnlyVariables(Text): # returns true if text contains only variables
    s = ""
    tmp = Text
    for i in range(len(Text)):
        s = s + Text[i]
        if s in variables:
            tmp = tmp.replace(s, "")
            s = ""
    if len(tmp) > 0:
        return False
    else:
        return True

def startWithVariable(Text): # returns true if text starts with a variable, False else
    s = ""
    for i in range(len(Text)):
        s = s + Text[i]
        if s in variables:
            return True, s
    return False

def rule1(node): # checks if both sides start with terminalsymbol
    tmp = Node()


    if (startWithVariable(node.LHS) == False) and (startWithVariable(node.RHS) == False):
        if node.LHS[0] == node.RHS[0]:# if they are the same delete it
            tmp.LHS = node.LHS[1:]#delete first char on both sides
            tmp.RHS = node.RHS[1:]
            tmp.displayText = tmp.LHS + " = " + tmp.RHS
            if graph.has_node(tmp.displayText) == False:
                if len(tmp.displayText) == len(node.displayText):
                    k = graph.nodes[node.displayText]
                    k = k['group']
                    graph.add_node(tmp.displayText, group=k)
                else:
                    graph.add_node(tmp.displayText, group=count[0])
                    count[0] = count[0] + 1
                currentNodes.append(tmp)
            graph.add_edge(node.displayText, tmp.displayText, label="rule1")# adds node if not already there
        else: #if not the same stop, ist not solvable from there
            return


def rule2(node):# rule 2; if the starting letter is a variable and it is empty
    newNode = Node()
    newNode1 = Node()
    kalu = currentNodes
    if startWithVariable(node.LHS):# Lefthandside starts with variable
        dummy, var = startWithVariable(node.LHS)
        newNode.LHS = node.LHS.replace(var, "")
        newNode.RHS = node.RHS.replace(var, "")
        newNode.displayText = newNode.LHS + " = " + newNode.RHS
        if graph.has_node(newNode.displayText) == False:
            if len(newNode.displayText) == len(node.displayText):
                k = graph.nodes[node.displayText]
                k = k['group']
                graph.add_node(newNode.displayText, group=k)
            else:
                graph.add_node(newNode.displayText, group=count[0])
                count[0] = count[0] + 1
            currentNodes.append(newNode)
        graph.add_edge(node.displayText, newNode.displayText, label="rule2")
    if startWithVariable(node.RHS):
        dummy, var = startWithVariable(node.RHS)
        newNode1.LHS = node.LHS.replace(var, "")
        newNode1.RHS = node.RHS.replace(var, "")
        newNode1.displayText = newNode1.LHS + " = " + newNode1.RHS
        if graph.has_node(newNode1.displayText) == False:
            if len(newNode1.displayText) == len(node.displayText):
                k = graph.nodes[node.displayText]
                k = k['group']
                graph.add_node(newNode1.displayText, group=k)
            else:
                graph.add_node(newNode1.displayText, group=count[0])
                count[0] = count[0] + 1
            currentNodes.append(newNode1)
        graph.add_edge(node.displayText, newNode1.displayText, label="rule2")


def rule3(node): #rule 3; if the starting letter is a variable and the other a nonvariable prefix
    tmp = Node()
    tmp1 = Node()
    if startWithVariable(node.LHS) and (startWithVariable(node.RHS) == False):
        dummy, var = startWithVariable(node.LHS)
        tmp.LHS = node.LHS.replace(var, node.RHS[0] + '' + var)# terminal is prefix of that variable
        tmp.LHS = tmp.LHS[1:] # first letter will then be the same, so it will be gone due to rule 1
        tmp.RHS = node.RHS.replace(var, node.RHS[0] + '' + var)
        tmp.RHS = tmp.RHS[1:]
        tmp.displayText = tmp.LHS + " = " + tmp.RHS
        if graph.has_node(tmp.displayText) == False:
            if len(tmp.displayText) == len(node.displayText):
                k = graph.nodes[node.displayText]
                k = k['group']
                graph.add_node(tmp.displayText, group=k)
            else:
                graph.add_node(tmp.displayText, group=count[0])
                count[0] = count[0] + 1
            currentNodes.append(tmp)
        graph.add_edge(node.displayText, tmp.displayText, label="rule3")
    if (startWithVariable(node.LHS) == False) and startWithVariable(node.RHS):
        dummy, var = startWithVariable(node.RHS)
        tmp1.RHS = node.RHS.replace(var, node.LHS[0] + '' + var)
        tmp1.RHS = tmp1.RHS[1:]
        tmp1.LHS = node.LHS.replace(var, node.LHS[0] + '' + var)
        tmp1.LHS = tmp1.LHS[1:]
        tmp1.displayText = tmp1.LHS + " = " + tmp1.RHS
        if graph.has_node(tmp1.displayText) == False:
            if len(tmp1.displayText) == len(node.displayText):
                k = graph.nodes[node.displayText]
                k = k['group']
                graph.add_node(tmp1.displayText, group=k)
            else:
                graph.add_node(tmp1.displayText, group=count[0])
                count[0] = count[0] + 1
            currentNodes.append(tmp1)
        graph.add_edge(node.displayText, tmp1.displayText, label="rule3")



def rule4(node): #rule 4; if both starts with variable but one is prefix of the other
    tmp = Node()
    tmp1 = Node()
    if startWithVariable(node.LHS) and startWithVariable(node.RHS):
        dummy, varLHS = startWithVariable(node.LHS)
        dummy, varRHS = startWithVariable(node.RHS)
        # RHS is prefix of LHS
        tmp.LHS = node.LHS.replace(varLHS, varRHS + '' + varLHS)
        tmp.RHS = node.RHS.replace(varLHS, varRHS + '' + varLHS)
        l = len(varRHS)
        tmp.LHS = tmp.LHS[l:]#due to rule 1 prefix can be eliminated
        tmp.RHS = tmp.RHS[l:]
        tmp.displayText = tmp.LHS + " = " + tmp.RHS
        if graph.has_node(tmp.displayText) == False:
            if len(tmp.displayText) == len(node.displayText):
                k = graph.nodes[node.displayText]
                k = k['group']
                graph.add_node(tmp.displayText, group=k)
            else:
                graph.add_node(tmp.displayText, group=count[0])
                count[0] = count[0] + 1
            currentNodes.append(tmp)
            graph.add_edge(node.displayText, tmp.displayText, label="rule4")
        else:
            data = graph.get_edge_data(node.displayText, tmp.displayText)

            if not data == None:
                label = data['label'] + "/rule4"
            else: label = "rule4"
            graph.add_edge(node.displayText, tmp.displayText, label=label)
        # LHS is prefix of RHS
        tmp1.LHS = node.LHS.replace(varRHS, varLHS + '' + varRHS)
        tmp1.RHS = node.RHS.replace(varRHS, varLHS + '' + varRHS)
        l = len(varLHS)
        tmp1.LHS = tmp1.LHS[l:]#due to rule 1 prefix can be eliminated
        tmp1.RHS = tmp1.RHS[l:]
        tmp1.displayText = tmp1.LHS + " = " + tmp1.RHS
        if graph.has_node(tmp1.displayText) == False:
            if len(tmp1.displayText) == len(node.displayText):
                k = graph.nodes[node.displayText]
                k = k['group']
                graph.add_node(tmp1.displayText, group=k)
            else:
                graph.add_node(tmp1.displayText, group=count[0])
                count[0] = count[0] + 1
            currentNodes.append(tmp1)
            graph.add_edge(node.displayText, tmp1.displayText, label="rule4")
        else:
            data1 = graph.get_edge_data(node.displayText, tmp1.displayText)
            label1 = "rule4"
            graph.add_edge(node.displayText, tmp1.displayText, label=label1)


def buildGraph():
    while len(currentNodes) > 0:
        kal = currentNodes
        node = currentNodes[0]
        if node.LHS == "" and node.RHS == "":
            currentNodes.pop(0)
            continue
        elif node.LHS == "":
            if OnlyVariables(node.RHS):
                graph.add_edge(node.displayText, " = ", label="Rule2")
            currentNodes.pop(0)
            continue
        elif node.RHS == "":
            if OnlyVariables(node.LHS):
                graph.add_edge(node.displayText, " = ", label="Rule2")
            currentNodes.pop(0)
            continue
        rule1(node)
        rule2(node)
        rule3(node)
        rule4(node)
        currentNodes.pop(0)


def determineVariable(startNode, endNode, s):
    lhs, rhs = startNode.split("=")
    lhs = lhs[0:len(lhs)-1]
    rhs = rhs[1:]
    if s == "rule3":
        if startWithVariable(lhs):
            dummy, s = startWithVariable(lhs)
            tmp = variables.index(s)
            assignments[tmp] = assignments[tmp] + rhs[0]
        elif startWithVariable(rhs):
            dummy, s = startWithVariable(rhs)
            tmp = variables.index(s)
            assignments[tmp] = assignments[tmp] + lhs[0]

def getAssignments(path):
    for j in range(len(variables)):
        assignments.append("")
    for i in range(len(path) - 1):
        p = graph.get_edge_data(path[i], path[i + 1])
        s = ""
        for val in p.values():
            s = val
            # print(s)
        determineVariable(path[i], path[i + 1], s)
    solvable = True
    print(solvable)


def makeNet(no, solvable, path):
    net = Network(height='800px', width='1000px', notebook=True, directed=True)
    no.displayText = no.displayText.replace(":", "-")
    k = no.displayText
    net.from_nx(graph)

    if solvable:
        for node in net.nodes:
            s = node["id"]
            if s in path:
                node.update(shape='triangle')
    for n in net.nodes:
        n['size'] = len(n['label']) * 2

    for e in net.edges:
        if len(e['from']) == len(e['to']):
            e.update({'size': 5})
        else:
            e.update({'size': 1})

    if solvable:
        for i in range(len(variables)):
            if assignments[i] != "":
                print(variables[i] + " = " + assignments[i])

    net.show_buttons(filter_=['configure', 'physics', 'layout'])

    s = "./output/" + no.displayText + ".html"
    net.show(s)


def performTransforms(LHS, RHS):

    n = Node()
    n.LHS = LHS
    n.RHS = RHS
    n.displayText = LHS + " = " + RHS
    graph.add_node(n.displayText, group=0)
    currentNodes.append(n)
    buildGraph()
    ok = variables
    solvable = False
    path = ""
    if graph.has_node(" = "):
        path = nx.shortest_path(graph, n.displayText, " = ")
        getAssignments(path)
        solvable = True
    else:
        print("not solvable")
    makeNet(n, solvable, path)
    size = len(graph.edges)
    g_tmp = nx.Graph(graph)
    diameter = nx.diameter(g_tmp)
    g_tmp = graph
    count = 0
    while not nx.is_directed_acyclic_graph(g_tmp):
        cycleEdges = nx.find_cycle(g_tmp)
        pl = cycleEdges[0]
        k1 = pl[0]
        k2 = pl[1]
        g_tmp.remove_edge(k1, k2)
        count += 1

    input = n.displayText + "," + str(size) + "," + str(diameter) + "," + str(solvable) + "\n"

    F = open("devops.txt", "a")
    F.writelines(input)
    F.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <string1> <string2>")
        sys.exit(1)

        # Get the input strings from command-line arguments
    LHS = sys.argv[1]
    RHS = sys.argv[2]
    performTransforms(LHS, RHS)
if __name__ == "__main__":
    main()