# let's make a program that helps us with sectional warping
# many drafts provide: 
# EPI, total width in reed, and striping order 
# but we need to know what yarn to use for each section 
# which may differ from loom to loom, but our loom has 2" sections 

"""
we should consider: 
non-multiples of 2" wide warps 
    extra should be evenly distributed on end sections 

we need a minimum of 2" wide strips, they can be 2.1 or 2.2" etc. but not less 

how will we provide input? 
"""

# input: number sections 
# color sequence 
# assume: letter###

"""
8 
A8 B48 C6 A30 B6 C18 A6 B78 C6 A48 B6 C31 
"""

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

""""""


"""
have to interpret the sequence in a meaningful way 

but also have to determine how many ends are in a section 

probably should: extract total ends from sequence 
(todo compare to additional input)
"""

total_ends = 0
warp_color_sequence = []

ends = 0

# create total sequence 
for stripe in input_sequence:
    # pdb.set_trace()
    ends = int(re.search(r'\d+', stripe).group(0))
    color = re.search(r'[a-zA-Z]+', stripe).group(0)
    total_ends += ends
    for end in range(0,ends):
        warp_color_sequence.append(color)

# determine number of ends per section 
approximate = total_ends // number_sections 
modulo = total_ends % number_sections

# create first version of sections, with minimum number of ends 
all_section_number_threads = [approximate]*number_sections


# we will distribute the modulo, if any, across sections evenly, working from the outside in, alternating sides 
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

        # reset indexes if needed
        if left_index > halfway:
            left_index = 0

        if right_index < halfway:
            right_index = len(all_section_number_threads)

        if modulo == 1:
            all_section_number_threads[left_index] += 1
            modulo -= 1

"""now we are ready to slice warp sequence"""

# needs to be ordered, needs to be consolidated color + number combinations 
# ex A 3, B 6, A 8, C 7 
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
