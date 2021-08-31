import numpy as np
import math

lines=[]

minLayerHeight = 0.2
maxLayerHeight = 0.4
Layers = 20

x0=0
y0=0
z0=0

for NoOfLayers in range(0, Layers):
    lines.append([])
    print(NoOfLayers)
    for y1 in range(0, 30):
        Y1=y1
        if (NoOfLayers % 2) == 0:
            Y1 = 30 - Y1
            y1=(29-y1)*0.5
        else:
            y1 = y1 * 0.5
        print(y1)
        for x1 in range(0, 55,2):
            # print(x1)
            if (Y1 % 2) == 0:
                x1=54-x1
            # print(x1)
            if (Y1>14):
                Y1 = 30-Y1
            t = math.acos((x1-29)/(30+Y1))
            # print(t)
            z1 = (10*(NoOfLayers+1)/Layers)*(math.sin(t))
            # print(z1)
            lines[NoOfLayers].append([x0, y1, z0, x1, y1, z1])
            x0 = x1
            z0 = z1
            # print(x0)

print(lines)

bedWidth=300
extrudeRate = 0.05

f = open("test1" + ".gcode", 'w')
f.write("M109 S210.000000\n")
f.write(";Start GCode\n")
f.write("G28 X0 Y0 Z0\n")
f.write("G92 E0\n")
f.write("G29\n")

f.write("M82 ;absolute extrusion mode\n")
f.write("M201 X500.00 Y500.00 Z100.00 E5000.00 ;Setup machine max acceleration\n")
f.write("M203 X500.00 Y500.00 Z10.00 E50.00 ;Setup machine max feedrate\n")
f.write("M204 P500.00 R1000.00 T500.00 ;Setup Print/Retract/Travel acceleration\n")
f.write("M205 X8.00 Y8.00 Z0.40 E5.00 ;Setup Jerk\n")
f.write("M220 S100 ;Reset Feedrate\n")
f.write("M221 S100 ;Reset Flowrate\n")

f.write("G92 E0 ;Reset Extruder\n")
f.write("G1 Z2.0 F3000 ;Move Z Axis up\n")
f.write("G1 X10.1 Y20 Z0.28 F5000.0 ;Move to start position\n")
f.write("G1 X10.1 Y200.0 Z0.28 F1500.0 E15 ;Draw the first line\n")
f.write("G1 X10.4 Y200.0 Z0.28 F5000.0 ;Move to side a little\n")
f.write("G1 X10.4 Y20 Z0.28 F1500.0 E30 ;Draw the second line\n")
f.write("G92 E0 ;Reset Extruder\n")
f.write("G1 Z2.0 F3000 ;Move Z Axis up\n")

origin = bedWidth / 2  # origin
layer = 1  # current layer/slice
E = 0  # extrusion accumulator
layerHeight=0.2
CurrentLayer=0

for line in lines:

    f.write(";Layer " + str(layer) + " of " + str(len(lines)) + "\n")

    # fan
    if (layer == 2):
        f.write("M106 S127\n")
    if (layer == 3):
        f.write("M106 S255\n")

    for px0,py0,pz0,px1,py1,pz1 in line:
        # move to start of line
        f.write("G0 F1000 X" + str(origin + px0) + " Y" + str(origin + py0) + " Z" + str(pz0) + "\n")
        # move to end while extruding

        # Calculate the distance
        dist = math.sqrt(pow(px1 - px0, 2) + pow(py1 - py0, 2) + pow(pz1 - pz0, 2))
        # print(pz1 - pz0)
        # E += ((4*layerHeight*1.2*dist)/(3.14*0.4))/(3.14*1.75*1.75/4))
        E += dist * extrudeRate * (0.4 + (pz1/(maxLayerHeight*layer)))
        # print(0.2 + (pz1/(maxLayerHeight*layer)))
        # print(pz1)
        # E += dist * extrudeRate
        f.write("G1 F600 X" + str(origin + px1) + " Y" + str(origin + py1) + " Z" + str(pz1) + " E" + str(E) + "\n")
    layer += 1

#postamble
f.write("M140 S0\n")
f.write("M107\n")
f.write("G91 ;Relative positioning\n")
f.write("G1 E-2 F2700 ;Retract a bit\n")
f.write("G1 E-2 Z0.2 F2400 ;Retract and raise Z\n")
f.write("G1 Z10 ;Raise Z more\n")
f.write("G90 ;Absolute positionning\n")
f.write("M106 S0 ;Turn-off fan\n")
f.write("M104 S0 ;Turn-off hotend\n")
f.write("M140 S0 ;Turn-off bed\n")
f.write("M84 X Y E ;Disable all steppers but Z\n")
f.write("M82 ;absolute extrusion mode\n")
f.write("M104 S0\n")
f.write(";End of Gcode\n")