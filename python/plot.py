import matplotlib.pyplot as plt

y0_values = []
y1_values = []
y2_values = []
y3_values = []
y4_values = []
y5_values = []
y6_values = []
y7_values = []

x_values = []

with open("[Insert Directory]", "r") as file:
    for count, line in enumerate(file):
        line = line.strip()
        if line:
            value0 = float(line.split(",")[0])
            value1 = float(line.split(",")[1])
            value2 = float(line.split(",")[2])
            value3 = float(line.split(",")[3])
            value4 = float(line.split(",")[4])
            value5 = float(line.split(",")[5])
            value6 = float(line.split(",")[6])
            value7 = float(line.split(",")[7])
            value8 = float(line.split(",")[8])
            y0_values.append(value0)  
            y1_values.append(value1)
            y2_values.append(value2)
            y3_values.append(value3)
            y4_values.append(value4)
            y5_values.append(value5)
            y6_values.append(value6)
            y7_values.append(value7)
            x_values.append(value8)

fig, (elec0, elec1, elec2, elec3, elec4, elec5, elec6, elec7) = plt.subplots(8)
fig.suptitle('Vertically stacked subplots')
elec0.plot(x_values, y0_values)
elec1.plot(x_values, y1_values)
elec2.plot(x_values, y2_values)
elec3.plot(x_values, y3_values)
elec4.plot(x_values, y4_values)
elec5.plot(x_values, y5_values)
elec6.plot(x_values, y6_values)
elec7.plot(x_values, y7_values)
fig.tight_layout(pad=0.005)
fig.savefig("my_plot.jpg", format='jpg', dpi=300)
