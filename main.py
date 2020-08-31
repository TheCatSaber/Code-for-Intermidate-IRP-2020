#====Imports====#

import time
import gc
from config_import import config_imports
from colouring_algorithms import greedy_colouring, dsatur_colouring
from random_graphs import random_graph, erdos_renyi
from colouring_orders import random_ordering, degree_ordering
from brute_force_colouring import (
    product_brute_force_colouring,
    custom_brute_force_colouring
)
import colouring_class
from output import output_graph


#====Main Function====#

def run_once():
    """Main function, does:
        graph creation;
        various colourings of the graph;
        output."""
    
    # CONSTANTS get
    # TIMES_TO_RUN not needed since it is known that
    # it is one if run_once() is called.
    global GRAPH_SIZE, RANDOM_GRAPH_EDGE_NUMBER
    global ERDOS_RENYI_P, COLOURING_TO_SHOW, SHOW_LABELS
    global RUN_BRUTE_FORCE, USE_ERDOS_RENYI
    
    # Create the graph, using the specified method and parameters.
    if USE_ERDOS_RENYI:
        graph = erdos_renyi(GRAPH_SIZE, ERDOS_RENYI_P)
    else:
        graph = random_graph(GRAPH_SIZE, RANDOM_GRAPH_EDGE_NUMBER)

    # Print information about the graph.
    print("Vertices:")
    print(graph.nodes())
    print("Edges:")
    print(graph.edges())

    # Instantiate instances of colouring_class.Colouring
    # for each colouring algorithm.
    
    random_greedy = colouring_class.Colouring(
        "Random greedy", greedy_colouring, "randomGreedy",
        True, random_ordering)

    degree_greedy = colouring_class.Colouring(
        "Degree greedy", greedy_colouring, "degreeGreedy",
        True, degree_ordering)

    dsatur = colouring_class.Colouring(
        "DSatur", dsatur_colouring, "DSatur",
        preserve_capitalisation=True)
    
    if RUN_BRUTE_FORCE:
        product_brute_force = colouring_class.Colouring(
            "Product brute force",
            product_brute_force_colouring,
            "productBruteForce")

        custom_brute_force = colouring_class.Colouring(
            "Custom brute force",
            custom_brute_force_colouring,
            "customBruteForce")

    # Default case for output_colouring is None
    # if COLOURING_TO_SHOW from graphs.config is invalid.
    output_colouring = None

    # Run each colouring on the graph and print out
    # the information about it.
    for colouring in colouring_class.colouring_object_list:
        colouring.main_colouring_function(graph)
        
        # Assign the desired colouring to output_colouring.
        if colouring.config_name == COLOURING_TO_SHOW:
            output_colouring = colouring.colouring

    # Error message to say that there was an invalid COLOURING_TO_SHOW.
    if output_colouring == None and COLOURING_TO_SHOW != None:
        print("Invalid colouringToShow in graphs.config. " \
              "Using no colouring in output.")

    # Create and display output picture.
    output_graph(graph, output_colouring, SHOW_LABELS)


colouring_repeated_objects_list = []

def run_many_times():
    """Run the colourings many times."""
    
    # Get CONSTANTS.
    # COLOURING_TO_SHOW and SHOW_LABELS are not needed
    # since we don't have an output figure.
    global GRAPH_SIZE, RANDOM_GRAPH_EDGE_NUMBER
    global ERDOS_RENYI_P, USE_ERDOS_RENYI
    global RUN_BRUTE_FORCE, TIMES_TO_RUN
    
    random_greedy = colouring_class.ColouringRepeated(
        "Random greedy", greedy_colouring, "randomGreedy",
        True, random_ordering)
    
    degree_greedy = colouring_class.ColouringRepeated(
        "Degree greedy", greedy_colouring, "degreeGreedy",
        True, degree_ordering)
    
    dsatur = colouring_class.ColouringRepeated(
        "DSatur", dsatur_colouring, "DSatur",
        preserve_capitalisation=True)

    if RUN_BRUTE_FORCE:
        product_brute_force = colouring_class.ColouringRepeated(
            "Product brute force",
            product_brute_force_colouring,
            "productBruteForce")

        custom_brute_force = colouring_class.ColouringRepeated(
            "Custom brute force",
            custom_brute_force_colouring,
            "customBruteForce")
    
    # Disable garbage collection so better comparison
    # (like in the timeit module).
    gc.disable()
    for counter in range(TIMES_TO_RUN):
        
        # Create graph.
        if USE_ERDOS_RENYI:
            graph = erdos_renyi(GRAPH_SIZE, ERDOS_RENYI_P)
        else:
            graph = random_graph(
                GRAPH_SIZE, RANDOM_GRAPH_EDGE_NUMBER)
        # Run each colouring on the graph.
        for object_ in colouring_class.colouring_object_list:
            object_.main_colouring_function(graph)
    gc.enable()
    for object_ in colouring_class.colouring_object_list:
        object_.print_information(TIMES_TO_RUN)
        

if __name__ == "__main__":
    # graphs.config imports
    # Default values
    GRAPH_SIZE = 6
    RANDOM_GRAPH_EDGE_NUMBER = 2
    ERDOS_RENYI_P = 0.5
    COLOURING_TO_SHOW = None
    SHOW_LABELS = True
    USE_ERDOS_RENYI = True
    RUN_BRUTE_FORCE = True
    TIMES_TO_RUN = 1
    
    # Perform import.
    (
        GRAPH_SIZE,
        RANDOM_GRAPH_EDGE_NUMBER,
        ERDOS_RENYI_P,
        COLOURING_TO_SHOW,
        SHOW_LABELS,
        USE_ERDOS_RENYI,
        RUN_BRUTE_FORCE,
        TIMES_TO_RUN,
    ) = config_imports(
        GRAPH_SIZE,
        RANDOM_GRAPH_EDGE_NUMBER,
        ERDOS_RENYI_P,
        COLOURING_TO_SHOW,
        SHOW_LABELS,
        USE_ERDOS_RENYI,
        RUN_BRUTE_FORCE,
        TIMES_TO_RUN,
    )
        
    if TIMES_TO_RUN == 1:
        run_once()
    elif TIMES_TO_RUN > 1:
        run_many_times()
    else:
        print("An error with " \
              "TIMES_TO_RUN has occurred. " \
              "Please make an issue on GitHub.")
