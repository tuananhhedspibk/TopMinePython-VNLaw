import os
import sys
import numpy
import math
import matplotlib.pyplot as plt
import networkx as nx

sys.path.insert(0, "/app")

class AHCTC:
  def __init__(self, ipt_data):
    self.input_file_name = ipt_data
    self.dataset = None
    self.d_p_c_l = []
    self.d_p_p_l = []
    self.dataset_size = 0
    self.dimension = 0
    self.T = None
    self.clusters = None
  
  def initialize(self):
    if not os.path.isfile(self.input_file_name):
      self.quit("Input file doesn't exist or it's not a file")

    self.dataset, self.T, self.clusters, self.d_p_c_l, self.d_p_p_l = self.load_data(self.input_file_name)
    self.dataset_size = len(self.dataset)

    if self.dataset_size == 0:
      self.quit("Input file doesn't include any data")

    self.dimension = len(self.d_p_c_l[0])

    if self.dimension == 0:
      self.quit("Dimension for dataset cannot be zero")

  def sup(self, c_id, current_clusters):
    """
      get supertype of clusters
    """ 
    return current_clusters[c_id]["supertype"]

  def set_sup(self, n_c_id, current_clusters):
    c_s = 0
    tmp_proximity = float("+inf")
    centroid = [0.0] * self.dimension
    size = len(current_clusters[n_c_id]["data_points"])

    for idx in current_clusters[n_c_id]["data_points"]:
      dim_data = self.d_p_c_l[idx]
      for i in range(self.dimension):
        centroid[i] += float(dim_data[i])
    for i in range(self.dimension):
      centroid[i] /= size
    
    for idx in current_clusters[n_c_id]["data_points"]:
      dis = self.euclidean_distance(self.d_p_c_l[idx], centroid)
      if tmp_proximity > dis:
        tmp_proximity = dis
        c_s = idx
    current_clusters[n_c_id]["supertype"] = c_s

  def find_sup(self, sup_m):
    for idx in range(self.dataset_size):
      if self.T[idx][sup_m] == 1:
        return idx
    return -1

  def euclidean_distance(self, d_p_1, d_p_2):
    size = len(d_p_1)
    result = 0.0
    for i in range(size):
      f1 = float(d_p_1[i])
      f2 = float(d_p_2[i])
      tmp = f1 - f2
      result += pow(tmp, 2)
    result = math.sqrt(result)
    return result

  def agglomerative_hierarchical_clustering(self):
    current_clusters = self.clusters

    while len(current_clusters) > 1:
      tmp_proximity =  float("+inf")
      ci = 0
      cj = 0
      # find mi and mj in M with maximum proximity(sup(mi), sup(mj))
      for c_id, data in current_clusters.items():
        for c_id_1, data_1 in current_clusters.items():
          if c_id != c_id_1:
            tmp_mi = self.sup(c_id, current_clusters)
            tmp_mj = self.sup(c_id_1, current_clusters)
            dis = self.euclidean_distance(self.d_p_c_l[tmp_mi], self.d_p_c_l[tmp_mj])
            if tmp_proximity > dis:
              ci = c_id
              cj = c_id_1
              tmp_proximity = dis

      c_ids_l = [ci, cj]
      # find max key in current_clusters
      n_c_id = max(current_clusters, key=int) + 1
      current_clusters[n_c_id] = {}

      # merge mi and mj as m and add m to M
      current_clusters[n_c_id]["data_points"] = []
      for c_id, data in current_clusters.items():
        if len(c_ids_l) > 0:
          if c_id in c_ids_l:
            for id in current_clusters[c_id]["data_points"]:
              current_clusters[n_c_id]["data_points"].append(id)
            c_ids_l.remove(c_id)
        else:
          break
      
      self.set_sup(n_c_id, current_clusters)
      sup_m = self.sup(n_c_id, current_clusters)
      sup_ci = self.sup(ci, current_clusters)
      sup_cj = self.sup(cj, current_clusters)

      # delete mi and mj from M
      del current_clusters[ci]
      del current_clusters[cj]

      if sup_m == sup_ci:
        self.T[sup_m][sup_cj] = 1
      elif sup_m == sup_cj:
        self.T[sup_m][sup_ci] = 1
      else:
        k = self.find_sup(sup_m)
        if k > -1:
          self.T[k][sup_m] = 0
          for g in range(self.dataset_size):
            if self.T[sup_m][g] == 1:
              self.T[sup_m][g] = 0
              self.T[k][g] = 1
          self.T[sup_m][sup_ci] = 1
          self.T[sup_m][sup_cj] = 1

    return current_clusters

  def show_graph_with_labels(self):
    rows, cols = numpy.where(self.T == 1)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    nx.draw(gr, node_size=500, with_labels=True)
    plt.show()

  def load_data(self, input_file_name):
    """
      dataset's structure:
      dataset[cluster_id]
      dataset[cluster_id][data_points]: list data points's id in cluster
      dataset[cluster_id][supertype]: supertype of cluster -
        same as mediod - centroid of cluster

      d_p_c_l: list coordinate of phrase in topic's space
      d_p_p_l: list phrase value of phrase

      T: adjacent matrix that store resultant taxonomy, tij = 1 when di is
        the direct supertype of dj
    """

    input_file = open(input_file_name, "r")
    dataset = {}
    d_p_c_l = []
    d_p_p_l = []
    
    id = 0
    for line in input_file:
      line = line.strip("\n").split("@")
      row = str(line[1])
      row = row.split(",")
      row = map(int, row)

      # First time, each data point is distinct cluster
      dataset[id] = {}
      dataset[id]["data_points"] = []
      dataset[id]["data_points"].append(id)
      dataset[id]["supertype"] = id

      d_p_c_l.append(row)
      d_p_p_l.append(str(line[1]))

      id += 1

    T = numpy.zeros(shape=(id, id))
    return dataset, T, dataset, d_p_c_l, d_p_p_l

  def quit(self, err_desc):
    raise SystemExit("\n" + "PROGRAM EXIT: " + err_desc + ", please check your input" + "\n")

if __name__ == "__main__":
  ipt_data = sys.argv[1]

  ahctc = AHCTC(ipt_data)
  ahctc.initialize()
  current_clusters = ahctc.agglomerative_hierarchical_clustering()
  numpy.savetxt('./topmine/output/T.csv', ahctc.T, fmt='%.0f')
  ahctc.show_graph_with_labels()
