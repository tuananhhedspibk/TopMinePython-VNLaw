import csv
import string
import json
import sys

sys.path.insert(0, "/app")

def loadNode():
	nodes_list = []
	with open("../topmine/output/keyword_topics_distribution.txt") as k_t_d_f:
		for line in k_t_d_f:
			node_text = line.split("@")[0]
			nodes_list.append(node_text)

	return nodes_list

def buildElementTree(idx, matrix, result, queue_processe, processed, d3j_nodes_list):
	if idx in processed:
		return findTreeChildren(idx, result, d3j_nodes_list)
	else :
		queue_processe.remove(idx)
		processed.append(idx)
		tree_build = {"name": d3j_nodes_list[idx], "children": []}
		children_tree = []
		for i, val in enumerate(matrix[idx]):
			if val == 1 :
				children_tree.append(buildElementTree(i, matrix, result, queue_processe, processed, d3j_nodes_list))
		tree_build["children"] = children_tree
		return tree_build

def findTreeChildren(idx, result, d3j_nodes_list):
	for i, res in enumerate(result):
		if res["name"] == d3j_nodes_list[idx]:
			return result.pop(i)
	return {"name": "null data", "children": []}

def loadData(d3j_nodes_list):
	matrix = [[]]
	processed = []
	queue_processe = []
	result = []

	with open("../topmine/output/T.csv") as csvfile:
		csvreader = csv.reader(csvfile, delimiter="\t")
		matrix = [[string.atoi(i) for i in line[0].split()] for line in csvreader]
	queue_processe = [i for i in xrange(len(matrix))]
	while len(queue_processe) > 0:
		processing_element = queue_processe[0]
		result.append(buildElementTree(processing_element, matrix, result, queue_processe, processed, d3j_nodes_list))
	return result

def dump_data(data):
  with open("graph.json", "w") as fp:
    json.dump(data, fp, indent=4, sort_keys=True)
	fp.close()

def main():
	d3j_data = {}
	d3j_nodes_list = loadNode()
	d3j_data = loadData(d3j_nodes_list)
	dump_data(d3j_data)

if __name__ == "__main__":
  main()
