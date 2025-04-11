import numpy as np
#import pytraj as pt
import networkx as nx
#import mdtraj as md
from networkx.algorithms.community import girvan_newman
from networkx.algorithms.community import modularity
import matplotlib.pyplot as plt


class Networkanalysis(object):
    def __init__(self,cutoff=None):
#          self.tra = trajectory
#          self.top = top
          self.cut = cutoff


    def adjacency_matrix(self,contact,covariance):
         self.contact=np.loadtxt(contact)
         self.covariance=np.loadtxt(covariance)
         adj_mat=np.zeros((np.shape(self.contact)[0],np.shape(self.contact)[1]))
         impindex=np.where(self.contact == 1)
         ic=zip(impindex[0],impindex[1])
         for i,j in ic:
             adj_mat[i,j]=-np.log(abs(self.covariance[i,j]))
 
         np.savetxt("adjacency_matrix.dat",adj_mat)

    def GirvanNewman(self,adj="adjacency_matrix.dat", maxcom=50):
        self.adjacency=np.loadtxt(adj)
        min_size=20
        n_residues=np.shape(self.adjacency)[1]
        G = nx.Graph()
        for i in range(n_residues):
            for j in range(i + 1, n_residues):
                if self.adjacency[i, j] != 0:
                   G.add_edge(i, j, weight=abs(self.adjacency[i, j]))

        communities_generator = girvan_newman(G)
        
        with open("Modularity_record.txt", "w") as g:

             for communities in communities_generator:
                 current_partition = [sorted(c) for c in communities]  # Sort for consistency
                 filtered_partition = [c1 for c1 in current_partition if len(c1) >= min_size]
#            all_partitions.append(current_partition)
                 num_communities = len(filtered_partition)
                 print(f"Number of communities: {len(filtered_partition)}")
        
                 with open(f"communities_{num_communities}.txt", "w") as f:
                      for comm_idx, community in enumerate(filtered_partition, 1):
                          cc=[x+1 for x in community]
                          f.write(f"Community {comm_idx}: {cc}\n")
                 
                 filtered_nodes = set().union(*filtered_partition)

                 # Create a subgraph with only those nodes and their edges
                 G_filtered = G.subgraph(filtered_nodes).copy()

                 mod = modularity(G_filtered, filtered_partition)
                 g.write(f"Total Communities: {num_communities}, Modularity: {mod:.4f}\n")

                 inter_weights = {}
                 with open(f"Community{num_communities}_weights.txt", "w") as h:
                     for i in range(num_communities):
                        for j in range(i + 1, num_communities):
                           comm1, comm2 = filtered_partition[i], filtered_partition[j]
                           total_weight = 0
                           for u in comm1:
                              for v in comm2:
                                 if G_filtered.has_edge(u, v):
                                    total_weight += G_filtered[u][v]['weight']
                                 if total_weight > 0:
                                    inter_weights[(i, j)] = total_weight
                     for (comm_i, comm_j), weightt in inter_weights.items():
                        h.write(f"Between Community {comm_i + 1} and {comm_j + 1}: {weightt:.4f}\n")

    # Stop if we reach max communities 
                 if len(current_partition) >= maxcom:
                   break


#traj = 'concatenated_NP_large.dcd'
#top = 'stripped.pic-med-non-phosphorylated-final.psf'

test = Networkanalysis(cutoff=0.45)
#test.contact_covariance()
test.adjacency_matrix("conmap_test_NP.dat","correlation_NP.dat")
test.GirvanNewman("adjacency_matrix.dat", maxcom=500)
