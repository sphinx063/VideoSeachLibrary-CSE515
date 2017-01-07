import math
import networkx as nx
import numpy
from operator import itemgetter
import imageio

inputFile = 'FinalData_k.gspc'

graph_dict = {}

charsToRemove = ['<','>','{','}']

out_links = {}
nodes = set()
weights = {}
threshold = 1e-4
graph = nx.Graph()
c = 0.9
max_iterations = 100
node_to_index_map = {}
neighbors = []
demo_video_path = 'P3DemoVideos'

def get_input_file():
    input_file = open(inputFile, "r")
    for line in input_file.readlines():
        line = removeChars(line)
        values = [val.strip() for val in line.split(',')]
        out_key = values[0] + ',' + values[1]
        nodes.add(out_key)
        if (out_links.get(out_key) == None):
            out_links[out_key] = []
        out_links[out_key].append(values[2] + ',' + values[3] + ',' + values[4])
    input_file.close()

def removeChars(line):
    for char in charsToRemove:
        line = line.replace(char, '')
    return line

def get_graph():
    #compute_weights()
    for node in nodes:
        graph.add_node(node)
    for node1 in out_links:
        neighbors = out_links[node1]
        for neighbor in neighbors:
            tokens = neighbor.split(',')
            node2 = tokens[0] + ',' + tokens[1]
            #w = weights[node1 + ';' + node2]
            w1 = float(tokens[2])
            graph.add_edge(node1, node2, weight=w1)

def compute_weights():
    for node in out_links:
        neighbors = out_links[node]
        weight_sum = 0
        for neighbor in neighbors:
            weight = float(neighbor.split(',')[2])
            weight_sum += weight
        for neighbor in neighbors:
            node2 = neighbor.split(',')[0] + ',' + neighbor.split(',')[1]
            weight = float(neighbor.split(',')[2])
            weights[node2 + ';' + node] = (float) (weight/weight_sum)
            weights[node + ';' + node2] = (float) (weight/weight_sum)

def ascos_similarity(graph):
    n = graph.number_of_nodes()
    sim = numpy.eye(n)
    sim_prev = numpy.zeros(shape = (n, n))
    node_ids = graph.nodes()
    
    for i in range(n):
       for j in range(n):
            if i == j:
               sim[i, j] = 1.0
    sim_prev = numpy.copy(sim)
 
    iteration_count = 0
    while(True):
       for i in range(n):
           weight = graph.degree(weight='weight')[node_ids[i]]
           for j in range(n):
               if i != j:
                  sim_ij = 0.0
                  if weight != 0:
                     for neighbor in neighbors[i]:
                         weight_k = graph[node_ids[i]][node_ids[neighbor]]['weight']
                         sim_ij += float(weight_k) * (1 - math.exp(-weight_k)) * sim_prev[neighbor, j]
                     sim[i, j] = c * sim_ij / weight
       if hasConverged(sim, sim_prev):
          break
       sim_prev = numpy.copy(sim)
       iteration_count += 1
       if iteration_count > max_iterations:
          break

    page_rank = {}

    #Compute Page Rank Values
    for j in range(n):
        node = node_ids[j]
        page_rank[node] = 0.0
        for i in range(n):
            page_rank[node] += sim[i,j]
        page_rank[node] = page_rank[node] / n

    result = sorted(page_rank.items(), key=itemgetter(1), reverse=True)
    num = int(m.strip())
    for p in range(0,num):
        print result[p]
        visualize_frame(p, result[p])
def get_node_neighbors(graph):
    node_ids = graph.nodes()
    for count, n in enumerate(node_ids): 
      node_to_index_map[n] = count
    neighbor_ids = []
    for node in node_ids:
      neighbor_ids.append(graph.neighbors(node))
    for neighbor_id in neighbor_ids:
      neighbors.append([node_to_index_map[n] for n in neighbor_id])

def hasConverged(sim, sim_prev):
    noOfRows = int(sim.shape[0])
    noOfColumns = int(sim.shape[1])
    for i in range(noOfRows):
      for j in range(noOfColumns):
        diff = math.fabs(sim[i,j] - sim_prev[i,j])
        if diff >= (float)(threshold):
          return False
    return True


def visualize_frame(index, item):
    tokens = item[0].split(',')
    reader = imageio.get_reader(demo_video_path + '/' + tokens[0])
    writer = imageio.get_writer("similar"+str(index)+".mp4", fps=reader.get_meta_data()['fps'])
    frame_index = 1
    for im in reader:
        if frame_index >= int(tokens[1]) and frame_index <= int(tokens[1]):
            writer.append_data(im[:, :, 1])
        frame_index = frame_index + 1
    writer.close()
    reader.close()

inputFile = raw_input("Enter the input file name").strip()
m = raw_input("Enter the value of m").strip()

get_input_file()
get_graph()
get_node_neighbors(graph)
ascos_similarity(graph)
