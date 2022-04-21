# CONSTANTS
tufting_height = -20
movement_height = 0

bed_width = 20
bed_height = 20

movement_feedrate = 400
tufting_feedrate = 300 

f = open("output.gcode", "w")

# Slicer functions - TODO move to own class ?

preamble = [
    "M17\n",
    #"G28\n", # Don't home again
    "G21\n",
    "G90\n",
    "M82\n",
    "G92 E0\n",
   # "G1 F{0}.000\n".format(g1_feedrate) # Set feedrate for G1 moves
]

f.writelines(preamble)

def slicer_wait():
    f.write("M400\n")

def slicer_enable_gun():
    f.write("M42 S0 P32\n")

def slicer_disable_gun():
    f.write("M42 S255 P32\n")

def slicer_retract():
    slicer_disable_gun()
    f.write("G1 Z{0}\n".format(movement_height))

def slicer_insert():
    slicer_disable_gun()
    f.write("G1 Z{0}\n".format(tufting_height))
    slicer_wait()
    slicer_enable_gun()

def slicer_non_tuft_move(x,y):
    slicer_retract()

    # Move to point
    f.write("G1 X{0} Y{1} F{2}\n".format(x, y, movement_feedrate))

def slicer_tuft_move(x,y):
    slicer_insert()

    # Move to point
    f.write("G1 X{0} Y{1} F{2}\n".format(x, y, tufting_feedrate))

    slicer_wait()

    slicer_disable_gun()


# Straight line
start_pos = (0,15)
end_pos = (0, 0)

# Generate tuftig code
slicer_non_tuft_move(start_pos[0], start_pos[1])
slicer_tuft_move(end_pos[0], end_pos[1])
slicer_retract()

f.close()