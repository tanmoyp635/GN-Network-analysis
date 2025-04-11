# GN-Network-analysis
This script performs network analysis using the Girvan-Newman algorithm to identify dynamic communities within a structure. To execute the script, you will need the following input files in the same directory:

conmap_test_NP.dat: the contact map file

correlation_NP.dat: the correlation matrix file

If you'd like to use different filenames, update the corresponding entries in the second-to-last line of the script.

To generate the correlation matrix, you can use the following command in cpptraj:

nginx
Copy
Edit
parm stripped.pic-med-non-phosphorylated-final.psf     # Topology file  
loadtraj concatenated_NP_large.dcd name TF             # Aligned and concatenated trajectory  
run  
crdaction TF matrix correl @CA,C4',FE1,FE2,FE3,FE4,MG,ZN byres out correlation_NP.dat
Note: You can modify the atom list (@CA,C4',FE1,...) as per your requirements.

To run the network analysis, simply execute:

python network_source_code.py

The script will generate several output files named communities$i.txt and Community$i_weights.txt, where $i corresponds to the community number. By default, the maximum number of communities is set to 500. You can change this by modifying the maxcom=500 parameter in the last line of the script.

Dependencies:
Make sure you have the following Python packages installed:
numpy
networkx
matplotlib

 
