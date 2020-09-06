"""2 brute force methods for optimal colouring of input graph.

product_brute_force_colouring uses itertools.product.
custom_brute_force_colouring uses a custom one, explained in detail __.
In summary, it counts in a variable base system,
but only tests if it is a valid colouring if it uses all the colours
from 1 to the number of colours being tested to prevent repeats.
"""
# Copyright (C) 2020 TheCatSaber

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

#====Imports====#

from itertools import product


#====Shared Functions====#

def validate_colouring(G, colouring):
    """Return True if colouring is a valid colouring of G, False otherwise."""
    for edge in G.edges():
        # edge[0] is the start vertex, edge[1] is the end vertex.
        # If the colours at the start and end of edge each are the same,
        # then colouring is not a valid colouring.
        if colouring[edge[0]] == colouring[edge[1]]:
            return False
    # All edges have different colours at either end, so valid colouring.
    return True


def colouring_list_to_dict(colouring_list, vertices):
    """Turn a list of colours (colouring_list) and a list of vertices
    (vertices) into a dictionary in the form vertex: colour.
    """
    colouring = {vertices[counter]: colouring_list[counter] \
        for counter in range(len(colouring_list))}
    return colouring


#====Product Brute Force====#

def product_brute_force_colouring(G):
    """Return dict colouring of G done by prodcut brute force method.
    
    Colourings generated by itertools.product.
    Iterates through all possible colourings,
    starting with the ones with 1 colour, then 2 and so on,
    checking if they are valid only if the colouring contains
    the highest possible colour (colours - 1).
    """
    size = len(G)
    vertices = list(G)

    #Start with 1 colour (0)
    colours = 1

    # While loop so keeps going until it eventually finds a colouring.
    while True:
        # Gives possible colourings for current amount of colours.
        # E.g. for 2 colours and 3 nodes, will give
        # 000, 001, 010, 011, 100, 101, 110, 111.
        colourings = product([i for i in range(colours)], repeat=size)
        for colouring_option in colourings:
            # Prevent repeats of colourings already checked
            # by checking if the highest possible colour is in
            # colouring_option which is colours - 1.
            if colours - 1 in colouring_option:
                
                # Convert to dict
                colouring = colouring_list_to_dict(colouring_option, vertices)
                
                # If the colouring is valid, return it
                if validate_colouring(G, colouring):
                    return colouring
                    
        # Increase number of colours being tested
        # and try again.
        colours += 1


#====Custom Brute Force Helpers and Main Function====#

def create_options(colours, size):
    """Creates the options for colouring_generator.
    
    colours -- number of colours being tested.
    size -- size of graph being tested."""
    # Counts up from 1 to colours.
    options_0 = [counter for counter in range(1, colours+1)]
    
    # The rest of the list has the value colours.
    # The length of the returned list needs to be size
    # and a vertex can't have more options than the number 
    # of colours being tested.
    options_1 = [colours] * (size - len(options_0))
    
    # Combine and return.
    full_options = options_0 + options_1
    return full_options
    
    
def colouring_generator(colouring_index, options):
    """Return a list of the colours.
    
    colouring_index -- counter for for loop (when iterating
    through all options).
    options -- from create_options."""
    colouring_list = []
    
    # Going through all list indices in reverse.
    for counter in range(len(options)-1, -1, -1):
        # Works as a variable base system.
        # Thus the last digit (for the returned list) is
        # the colouring_list % the base (options[counter]),
        # and the colouring_index to pass to the next stage is
        # the whole number // the base.
        colouring_list.append(colouring_index % options[counter])
        colouring_index = colouring_index // options[counter]
    # Reverse to aid explanation:
    # (So first vertex is always 0)
    colouring_list.reverse()
    return colouring_list
    

def check_all_colours_in_colouring_list(colours, colouring_list):
    """Return True if they are colours unique items in colouring_list.
    
    colours -- the number of items.
    colouring_list -- the list that needs to be checked it has enough
    unique items in.
    """
    if len(set(colouring_list)) == colours:
        return True
    return False
    

def custom_brute_force_colouring(G):
    """Return dict colouring of G done by acustom brute force method.
    
    The first vertex is always assigned the colour 0,
    the second vertex the colours 0 or 1,
    the third vertex the colours 0, 1 or 2 and so on.
    However, the vertices have a maximum number of options of colours
    (the number of colours currently being tested).
    Colourings are only checked if they contain all the colours
    from 0 to colours-1 (i.e. they have colours unique items).
    """
    vertices = list(G)
    size = len(G)

    # Start with 1 colour (0)
    colours = 1

    # While loop so keeps going until it eventually finds a colouring.
    while True:
        if colours <= size:
            try:
                # Create options
                options = create_options(colours, size)
            except:
                print("Error doing custom brute force colouring. " \
                      "Please make an issue on GitHub.")
                return None
        else:
            # The colouring will never require more
            # colours than there are vertices in G
            # Thus an error has occurred.
            print("No custom brut force colouring found. " \
                  "Please make an issue on GitHub.")
            return None
        
        # number_colourings is the number of possible colourings
        # there are to iterate through.
        number_colourings = 1
        for option in options:
            number_colourings *= option
        
        # Iterate through all possible colourings with colours colours.
        for counter in range(number_colourings):
            
            # Create colouring.
            colouring_list = colouring_generator(counter, options)
            
            # Prevent repeats of colourings already checked
            # by checking if all possible colours are in the colouring.
            if check_all_colours_in_colouring_list(colours, colouring_list):
                
                # Convert the list to a dict
                colouring = colouring_list_to_dict(colouring_list, vertices)
                
                # If the colouring is valid, return it
                if validate_colouring(G, colouring):
                    return colouring
                    
        # Increase number of colours being tested
        # and try again.
        colours+=1
