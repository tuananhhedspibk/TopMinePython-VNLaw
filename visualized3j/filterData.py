def filter():
  results = []
  k_vs_list = []
  forbiden_char = ["@", "#", "$", "%", "/", "(", "*", "-", "+", "\"", ":", "_"]
  with open("../topmine/output/keyword_topics_distribution.txt") as k_t_d_f:
    for line in k_t_d_f:
      k_v = line.split("@")[0]
      k_c = line.split("@")[1]
      if len(k_v.strip()) > 0:
        k_v = k_v.strip()
        if k_v[0] in forbiden_char or k_v[0] == ")":
          k_v = k_v.replace(k_v[0], "")
        if len(k_v) > 0:
          if k_v[len(k_v) - 1] in forbiden_char:
            k_v = k_v.replace(k_v[len(k_v) - 1], "")
          if len(k_v.strip()) > 1 and len(k_v) > 1:
            k_v = k_v.strip()
            if k_v not in k_vs_list:
              k_vs_list.append(k_v)
              item = k_v + "@" + k_c
              results.append(item)
  return results

def dump_data(data):
  fp = open("../topmine/output/keyword_topics_distribution.txt", "w")
  for line in data:
    fp.write("%s" % line)
  fp.close()

def main():
  data = filter()
  dump_data(data)

if __name__ == "__main__":
  main()
