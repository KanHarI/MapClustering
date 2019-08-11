# A heuristical solution to a specific case of set-covering problem

The problem I am trying to solve is finding a heuristical solution to the special case of set covering, when the elements in the sets are nodes in a graph. Coloring a single node colors also all connected nodes, and we are are trying to color the whole graph using a minimal amount of colorings.

# Our approach

We calculate the page rank ranking of all nodes in the graph, and attempt to find a coloring that color the nodes that are the least well-connected to other nodes. The value of each node is the sum of exponents of zero minus the page rank of all it's neighbors. We then choose the node with the highest value and remove it and all it's neighbors from the graph, and recalculate the page rank. The idea is that we want to remove "remote" nodes first and "central" nodes later as they are better connected.

# Results

This method was developed to solve an actual problem - finding data from a proximity based REST API containing information about various geographical positions, that returned results for all points of up to a given radius from the queried points. Querying this API was expensive, so we tried to minimize queries to it. This method resulted in vastly superior results to greedy querying the API.
