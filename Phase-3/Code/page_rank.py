import math
from operator import itemgetter
import networkx as nx
import imageio

inputFile = 'phase3_input_10_2.gspc'

graph_dict = {}

charsToRemove = ['<','>','{','}']

out_links = {} 
in_links = {}
nodes = set()
weights = {}
threshold = .000000001;
graph = nx.Graph()
m = 10
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
        in_key = values[2] + ',' + values[3]
        if (in_links.get(in_key) == None):
            in_links[in_key] = []
        in_links[in_key].append(values[0] + ',' + values[1] + ',' + values[4])
    input_file.close()

def removeChars(line):
    for char in charsToRemove:
        line = line.replace(char, '')
    return line

def get_weights():
    for node in nodes:
        graph.add_node(node)
    for node in in_links:
        neighbors = in_links[node]
        weight_sum = 0
        for neighbor in neighbors:
            weight = float(neighbor.split(',')[2])
            weight_sum += weight
        for neighbor in neighbors:
            tokens = neighbor.split(',')
            node2 = tokens[0] + ',' + tokens[1]
            w1 = float(tokens[2])
            weights[node2 + ';' + node] = (float) (w1/weight_sum)
            weights[node + ';' + node2] = (float) (w1/weight_sum)
            graph.add_edge(node, node2, weight=w1)

def compute_page_rank():
    node_list = list(nodes)
    num_of_nodes = len(node_list)    
    pr = {}
    prOld = {}
		
    for i in range(0,num_of_nodes):
        node = node_list[i]
	pr[node] = (float) (1.0/num_of_nodes);
	prOld[node] = (float) (1.0/num_of_nodes);

    c = 0.85;
    loop = 1;
		
    while (True):
        sinkPR = 0.0;

	for i in range(0,num_of_nodes):
            node = node_list[i]
	    if (out_links.get(node) == None) or (len(out_links[node]) == 0): # Sink nodes
		sinkPR += (float) (prOld[node]);

	for i in range(0,num_of_nodes):
            node = node_list[i]
	    pr[node] = (float) ((1.0 - c)/num_of_nodes);
	    pr[node] += (float) ((c*sinkPR)/num_of_nodes);
            if in_links.get(node) != None:
	        neighbors = in_links[node]
	        for j in range(0,len(neighbors)):
                    tokens = neighbors[j].split(',')
                    in_node = tokens[0] + ',' + tokens[1]
                    weight = weights[in_node + ';' + node]
                    pr[node] += (float) ((c * prOld[in_node] * weight)/len(out_links[in_node]))

	#Check for convergence
	if hasConverged(pr, prOld, node_list):
	    #print " Page Rank Iterations Done " + str(loop)
	    break;
	else:
	    for i in range(0,num_of_nodes):
                node = node_list[i]  
		prOld[node] = pr[node];
	loop = loop + 1

    result = sorted(pr.items(), key=itemgetter(1), reverse=True)
    num = int(m.strip())
    for p in range(0,num):
        print result[p]
        visualize_frame(p,result[p])

def hasConverged(pr, prOld, node_list):
    difference = 0;
    flag = True
    
    for node in node_list:
        difference = (float) (pr[node] - prOld[node]);
        if (math.fabs(difference) > (float)(threshold)):
             flag = False;
             break;
    return flag;

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

def compute_page_rank_using_networkx(graph):
    result = nx.pagerank(graph).items()
    num = int(m.strip())
    for p in range(0,num):
        print result[p]
        visualize_frame(p,result[p])

inputFile = raw_input("Enter the input file name").strip()

m = raw_input("Enter the value of m").strip()

get_input_file()

get_weights()

#compute_page_rank()

compute_page_rank_using_networkx(graph)
