In this project, the self-similarity of networks is examined used
simulations, in order to reproduce the results of [1]. In addition,
an application to real-world network data is provided -- in which the networks
are not self-similar! 

Different kinds of graphs (Erdos-Renyi, Barabasi-Albert, Watts-Strogatz)
are generated using the networkx package in python. The fractal model was
implemented from scratch [2]. 

The particular renormalization process I implemented is given in [3], the greedy
coloring algorithm (GCA). GCA takes as input a graph, and generates a 
renormalization flow. The file 'gca.py' generates graphs and runs GCA, then 
calculates the relative maximum degree, its variance, and the relative graph size 
for each stage of the process. For analysis, scaling exponents are calculated
and compared by performing GCA on graphs of varying node numbers 
('gca_analysis.ipynb'). More details are found in the report. 

References:
[1] Filippo Radicchi, José J Ramasco, Alain Barrat, and Santo Fortunato. Complex networks renormalization: Flows and fixed points. Physical review letters, 101(14):148701, 2008.

[2] Chaoming Song, Shlomo Havlin, and Hernán A Makse. Supplementary information for origins of fractality in the growth of complex networks. Nature Physics, 2(4):275, 2006.

[3] How to calculate the fractal dimension of a complex network: the box covering
algorithm. Journal of Statistical Mechanics: Theory and Experiment, 2007(03):P03006, 2007.



