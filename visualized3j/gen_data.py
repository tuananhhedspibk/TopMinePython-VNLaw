import json
import sys

sys.path.insert(0, "/home/mylaptop/Program/GR/LDA/TopMine")

def load_nodes_list():
  nodes = []
  with open("./topmine/output/keyword_topics_distribution.txt") as fp:
    for line in fp:
      keyword = line.split("@")[0]
      node = {}
      node["id"] = unicode(keyword, "utf-8")
      node["group"] = 1
      nodes.append(node)
  return nodes

def load_link(keywords):
  links = []
  ct = -1
  with open("./topmine/output/T.csv") as fp:
    for line in fp:
      ct += 1
      link_data = line.split(" ")
      for i in range(0, len(link_data)):
        if link_data[i] == "1":
          data = {}
          data["value"] = 3
          data["source"] = keywords[ct]["id"]
          data["target"] = keywords[i]["id"]
          links.append(data)
  return links

def dump_data(data):
  with open("graph.json", "w") as fp:
    json.dump(data, fp)

def main():
  d3j_data = {}
  nodes = load_nodes_list()
  links = load_link(nodes)
  d3j_data["nodes"] = nodes
  d3j_data["links"] = links

  dump_data(d3j_data)

if __name__ == "__main__":
  main()
