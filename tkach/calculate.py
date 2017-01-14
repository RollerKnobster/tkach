from copy import deepcopy
from graph_tool.all import *
import os


def calculate(array):
    elements = set()
    objects = dict()
    objects_list = dict()
    table = dict()

    for i, line in enumerate(array.split('\n'), start=1):
        objects[i] = set()
        objects_list[i] = list()
        for element in line.split(' '):
            if element not in objects[i]:
                objects[i].add(element.strip())
                objects_list[i].append(element.strip())
            if element not in elements:
                elements.add(element.strip())

    for i, the_object in enumerate(objects, start=1):
        table[i] = []
        for element in elements:
            if element in objects[i]:
                table[i].append(1)
            else:
                table[i].append(0)

    matrix = list()
    for x in range(len(objects)):
        line = list()
        for y in range(len(objects)):
            line.append(len(elements))
        matrix.append(line)

    for j in range(len(matrix)):
        for i in range(j + 1):
            matrix[i][j] = 0

    for i in range(len(matrix)):
        for j in range(i):
            for m in range(len(elements)):
                if table[i + 1][m] != table[j + 1][m]:
                    matrix[i][j] -= 1

    groups = dict()
    group_count = 1

    out_matrix = dict()

    for i, element in enumerate(deepcopy(matrix), start=1):
        out_matrix[i] = element

    while bool(sum([sum([matrix[i][j] for j in range(len(matrix))]) for i in range(len(matrix))])):
        groups[group_count] = set()
        maximum = 0

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] > maximum:
                    maximum = matrix[i][j]

        mem_i = 0
        mem_j = 0

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == maximum:
                    mem_i = i
                    mem_j = j
                    break
            if mem_i and mem_j:
                break

        groups[group_count].add(mem_i + 1)
        groups[group_count].add(mem_j + 1)

        def recursion(ti, tj):
            for k in range(len(matrix[0])):
                if matrix[ti][k] == maximum and (k + 1 not in groups[group_count]):
                    groups[group_count].add(k + 1)
                    recursion(ti, k)
            for k in range(len(matrix[0])):
                if matrix[k][tj] == maximum and (k + 1 not in groups[group_count]):
                    groups[group_count].add(k + 1)
                    recursion(k, tj)
            for k in range(len(matrix[0])):
                if matrix[tj][k] == maximum and (k + 1 not in groups[group_count]):
                    groups[group_count].add(k + 1)
                    recursion(tj, k)
            for k in range(len(matrix[0])):
                if matrix[k][ti] == maximum and (k + 1 not in groups[group_count]):
                    groups[group_count].add(k + 1)
                    recursion(k, ti)

        recursion(mem_i, mem_j)

        for e in groups[group_count]:
            for i in range(len(matrix)):
                matrix[i][e - 1] = 0
                matrix[e - 1][i] = 0

        group_count += 1

    def calculate_elements(groups):
        return_elements = dict()
        for group in groups:
            elements_in_group = set()
            for object in groups[group]:
                for element in objects[object]:
                    elements_in_group.add(element)
            return_elements[group] = elements_in_group
        return return_elements

    answers = list()

    def recursion_new(input_groups):
        elements_in_groups = calculate_elements(input_groups)
        sorted_groups = sorted(input_groups, key=lambda k: len(elements_in_groups[k]), reverse=True)
        detailed_groups = deepcopy(input_groups)
        # print "new recursion:"
        # print input_groups
        # print sorted_groups
        for i in range(len(sorted_groups)):
            the_group = sorted_groups[i]
            for group in sorted_groups:
                # print "iteration"
                # print sorted_groups
                # print str(group) + " " + str(the_group)
                if group in detailed_groups and the_group in detailed_groups:
                    if group != the_group and len(groups[group]) < len(groups[the_group]):
                        for object in input_groups[group]:
                            if objects[object].issubset(elements_in_groups[the_group]):
                                # print " ".join([str(the_group), "perekrivaye", str(object), "in", str(group)])
                                detailed_groups[the_group].add(object)
                                detailed_groups[group].remove(object)
                                if len(detailed_groups[group]) == 0:
                                    del detailed_groups[group]
                                recursion_new(detailed_groups)
        # print sorted_groups
        answers.append(detailed_groups)
        return detailed_groups

    recursion_new(groups)

    output_groups = answers[0]

    # print answers

    # print groups
    print output_groups

    print objects
    print objects_list

    def calculate_elements_to_list(groups):
        return_elements = dict()
        for group in groups:
            elements_in_group = list()
            for object in groups[group]:
                for element in objects_list[object]:
                    if element not in elements_in_group:
                        elements_in_group.append(element)
            return_elements[group] = elements_in_group
        return return_elements

    elements_in_groups_list = calculate_elements_to_list(output_groups)

    def enumerate_elements(elements_in_groups):
        enumerated = dict()
        for group in elements_in_groups:
            enumerated[group] = dict()
            for i, element in enumerate(elements_in_groups[group], start=1):
                enumerated[group][element] = i
        return enumerated

    elements_enumerated = enumerate_elements(elements_in_groups_list)

    print elements_enumerated

    relations_matrices = dict()

    print elements_in_groups_list

    graph_list = dict()

    vprop_strings = dict()

    for group in output_groups:
        graph = Graph()
        vprop_string = graph.new_vertex_property("string")
        relations_matrix = list()
        print "NEW MATRIX WITH DIMS: " + str(len(elements_in_groups_list[group]))
        for i in range(len(elements_in_groups_list[group])):
            line = list()
            for y in range(len(elements_in_groups_list[group])):
                line.append(0)
            relations_matrix.append(line)
        print relations_matrix
        for object in output_groups[group]:
            for j in range(len(objects_list[object]) - 1):
                if j != range(len(objects_list[object])):
                    if relations_matrix[elements_enumerated[group][objects_list[object][j]] - 1][elements_enumerated[group][objects_list[object][j + 1]] - 1] != 1:
                        graph.add_edge(elements_enumerated[group][objects_list[object][j]] - 1, elements_enumerated[group][objects_list[object][j + 1]] - 1)
                        vprop_string[elements_enumerated[group][objects_list[object][j]] - 1] = elements_in_groups_list[group][elements_enumerated[group][objects_list[object][j]] - 1]
                        vprop_string[elements_enumerated[group][objects_list[object][j+1]] - 1] = elements_in_groups_list[group][elements_enumerated[group][objects_list[object][j+1]] - 1]
                        relations_matrix[elements_enumerated[group][objects_list[object][j]] - 1][elements_enumerated[group][objects_list[object][j + 1]] - 1] = 1
        relations_matrices[group] = relations_matrix
        graph_list[group] = graph
        vprop_strings[group] = vprop_string

    print relations_matrices

    folder = "/Users/doorknob/dev/pythonVirtualEnvs/projects/tkach/tkach/static/graphs/"

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)

    for graph in graph_list:
        name = "static/graphs/graph_group_" + str(graph) + ".png"
        graph_draw(graph_list[graph], output=name, vertex_text=vprop_strings[graph], vertex_font_size=18,
                   vertex_size=50, edge_pen_width=5)



    return table, out_matrix, groups, elements, output_groups, relations_matrices, elements_in_groups_list
