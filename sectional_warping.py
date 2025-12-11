# let's make a program that helps us with sectional warping
# many drafts provide: 
# EPI, total width in reed, and striping order 
# but we need to know what yarn to use for each section 
# which may differ from loom to loom, but our loom has 2" sections 

"""
we should eventually consider: 
non-multiples of 2" wide warps 

we need a minimum of 2" wide strips, they can be 2.1 or 2.2" etc. but not less 
should check if distribution of extra threads puts us over this limit 

how will we provide input? 
"""

# input: 
# color and quantity  
# assume: letter###

import re
import pdb
from itertools import groupby
"""should be replaced by user inputs later"""

# for coastal linen tea towels
#number_sections = 8
#input_sequence = ["A8", "B48", "C6", "A30", "B6", "C18", "A6", "B78", "C6", "A48", "B6", "C31"] 

# for floral bouquet 
number_sections = 9
input_sequence = ["A547"]

total_ends = 0
warp_color_sequence = []

ends = 0

# create overall color sequence so we can group into sections later
for stripe in input_sequence:
    ends = int(re.search(r'\d+', stripe).group(0))
    color = re.search(r'[a-zA-Z]+', stripe).group(0)
    total_ends += ends
    for end in range(0,ends):
        warp_color_sequence.append(color)

# determine estimated number of ends per section 
# we need to distribute the modulo across our sections evenly later 
approximate = total_ends // number_sections 
modulo = total_ends % number_sections

all_section_number_threads = [approximate]*number_sections

# strategy: work outside in, one thread per section 
# at the halfway point, reset to the outside section 
if modulo != 0:
    
    left_index = 0
    right_index = len(all_section_number_threads) - 1

    halfway = len(all_section_number_threads) / 2
    while modulo > 0: 
        all_section_number_threads[left_index] += 1
        all_section_number_threads[right_index] += 1
        left_index += 1
        right_index -= 1 
        modulo -= 2

        # reset indexes if we've reached halfway 
        if left_index > halfway:
            left_index = 0

        if right_index < halfway:
            right_index = len(all_section_number_threads)

        if modulo == 1:
            all_section_number_threads[left_index] += 1
            modulo -= 1

#now we are ready to slice warp sequence
final_sections = [""]*number_sections

current_section_number = 0
section_start_index = 0

selected_threads = []

for section_length in all_section_number_threads:

    # slice from the start of our section to the end of the section 
    selected_threads = warp_color_sequence[section_start_index:section_start_index+section_length]

    # now group selected_threads properly 
    grouped = groupby(selected_threads)

    for color, amount in grouped: 
        final_sections[current_section_number] += color + ": " + str(len(list(amount))) + " \t "  
        
    # update everything for the next loop 
    current_section_number += 1
    section_start_index += section_length


for section in final_sections:
    print("Section: " + section[:-3])
