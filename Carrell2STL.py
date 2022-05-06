import numpy as np
from stl import mesh
from fileinput import filename
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

fileName='V1141Her_SMOOTH'
df = pd.read_csv(fileName+'.csv',header=None)
xs=range(max(df[df.columns[1]].tolist())+1)
ys=range(max(df[df.columns[0]].tolist())+1)
zs=df[df.columns[2]].tolist()
base=10 #[mm] base height
zs=[z+base for z in zs]

#4 coner verticies
#verticies = np.array([[xmin,ymin,0],[xmax,ymin,0],[xmax,ymax,0],[xmin,ymax,0]])
#    ── 
#   │  │
#    ┅┅>
#x axis on y min        0 ~ len(xs)-1
verticies = np.array([0,0,0],ndmin=2)
for x in range(1,len(xs)):
    verticies= np.append(verticies,[[xs[x],0,0]],axis=0)
print("Debug: xmin")
#    ┅┅> 
#   │  │
#    ──
#x axis on y min        len(xs) ~ 2*len(xs)-1
for x in range(0,len(xs)):
    verticies= np.append(verticies,[[xs[x],ys[-1]+1,0]],axis=0)
print("Debug: xmax")
#   ^── 
#   ┇  │
#    ──
#x axis on y min        2*len(xs) ~ 2*len(xs)+len(ys)
for y in range(0,len(ys)+1):
    verticies= np.append(verticies,[[0,y,0]],axis=0)
print("Debug: ymin")
#    ──^ 
#   │  ┇
#    ──
#y axis on x max        2*len(xs)+len(ys)+1 ~ 2*len(xs)+2*len(ys)+1
for y in range(0,len(ys)+1):
    verticies= np.append(verticies,[[xs[-1],y,0]],axis=0)
print("Debug: ymax")
# print(verticies[2*len(xs)+2*len(ys)-1])
# print(verticies[2*len(xs)-1])

# value points         2*len(xs)+2*len(ys)+2 ~ 2*len(xs)+2*len(ys)+len(zs)+1
for y in range(len(ys)):
    for x in range(len(xs)):   
        verticies= np.append(verticies,[[xs[x],ys[y],zs[y*len(xs)+x]]],axis=0)
    print("Debug: value points",y/len(ys)*100,"%")
print("Debug: value points")

# value points +1 on y        2*len(xs)+2*len(ys)+len(zs)+2 ~ 2*len(xs)+2*len(ys)+2*len(zs)+1
for y in range(len(ys)):
    for x in range(len(xs)):   
        verticies= np.append(verticies,[[xs[x],ys[y]+1,zs[y*len(xs)+x]]],axis=0)   
    print("Debug: value+1 points",y/len(ys)*100,"%")
print("Debug: value+1 points")

#==================FACES===========================================================================
#bottom surface
#   2       len(xs)
#   1 3     0   len(xs)-1

#   3 1     len(xs) 2*len(xs)-1
#     2             len(xs)-1
faces = np.array([[0,len(xs),len(xs)-1],[2*len(xs)-1,len(xs)-1,len(xs)]])
print("Debug: Botton surface")
#top surface
for y in range(len(ys)):
    for x in range(len(xs)-1):
        #   c d
        #   a b
        a=2*len(xs)+2*len(ys)+y*len(xs)+x+2
        b=2*len(xs)+2*len(ys)+y*len(xs)+x+1+2
        c=2*len(xs)+2*len(ys)+len(zs)+y*len(xs)+x+2
        d=2*len(xs)+2*len(ys)+len(zs)+y*len(xs)+x+1+2
        #   3
        #   1 2
        faces = np.append(faces,[[a,b,c]],axis=0)
        #   2 1
        #     3
        faces = np.append(faces,[[d,c,b]],axis=0)     
    print("Debug: top surface",y/len(ys)*100,"%")
print("Debug: top surface")

#top side surface
for y in range(len(ys)-1):
    for x in range(len(xs)-1):
        #   c d
        #   a b
        a=2*len(xs)+2*len(ys)+len(zs)+y*len(xs)+x+2
        b=2*len(xs)+2*len(ys)+len(zs)+y*len(xs)+x+1+2
        c=2*len(xs)+2*len(ys)+(y+1)*len(xs)+x+2
        d=2*len(xs)+2*len(ys)+(y+1)*len(xs)+x+1+2

        #   3
        #   1 2
        faces = np.append(faces,[[a,b,c]],axis=0)
        #   2 1
        #     3
        faces = np.append(faces,[[d,c,b]],axis=0)  
    print("Debug: top side surface",y/len(ys)*100,"%")
print("Debug: top side surface")

#walls
#x wall ymin
for x in range(len(xs)-1):
    #   c d
    #   a b
    a=x
    b=x+1
    c=2*len(xs)+2*len(ys)+x+2
    d=2*len(xs)+2*len(ys)+x+1+2

    #   3
    #   1 2
    faces = np.append(faces,[[a,b,c]],axis=0)
    #   2 1
    #     3
    faces = np.append(faces,[[d,c,b]],axis=0) 
print("Debug: xwall ymin")

#x wall y max
for x in range(len(xs)-1):
    #   c d
    #   a b
    
    a=len(xs)+2*len(ys)+2*len(zs)+x+2
    b=len(xs)+2*len(ys)+2*len(zs)+x+3
    c=len(xs)+x
    d=len(xs)+x+1
    #   3
    #   1 2
    faces = np.append(faces,[[a,b,c]],axis=0)
    #   2 1
    #     3
    faces = np.append(faces,[[d,c,b]],axis=0) 
print("Debug: xwall ymax")

#y wall x min
for y in range(len(ys)):
    #   c d
    #   a b
    a=2*len(xs)+y
    b=2*len(xs)+2*len(ys)+y*len(xs)+2
    c=2*len(xs)+y+1
    d=2*len(xs)+2*len(ys)+len(zs)+y*len(xs)+2
    #   3
    #   1 2
    faces = np.append(faces,[[a,b,c]],axis=0)
    #   2 1
    #     3
    faces = np.append(faces,[[d,c,b]],axis=0) 
print("Debug: y wall x min")

#y wall x max
for y in range(len(ys)):
    #   c d
    #   a b
    a=2*len(xs)+2*len(ys)+(y+1)*len(xs)-1+2
    b=2*len(xs)+len(ys)+1+y
    c=2*len(xs)+2*len(ys)+len(zs)+(y+1)*len(xs)-1+2
    d=2*len(xs)+len(ys)+y+2
    #   3
    #   1 2
    faces = np.append(faces,[[a,b,c]],axis=0)
    #   2 1
    #     3
    faces = np.append(faces,[[d,c,b]],axis=0) 
print("Debug: y wall x max")


# Create the mesh
#print(vertices[[3,7,6][1]]) [-1  1  1]
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    #print(i,f) #2 [0 4 7]
    for j in range(3):
        cube.vectors[i][j] = verticies[f[j],:]

# Write the mesh to file "cube.stl"
cube.save(fileName+'.stl')