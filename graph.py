import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np

#Set up the graph
fig, ax = plt.subplots()
fig.subplots_adjust(bottom = 0.2) #Move graph up so buttons have room
fig.suptitle("K-Means Clustering Visualization")
ax.set_title('Click to add data points') #Initially, the user is adding data points
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

#The x and y values of the data points
x_points = []
y_points = []
#The current x and y-values of the centroids
x_centroids = []
y_centroids = []
#List of cluster colors
colors = ["r", "g", "m","y","c", "pink", "orange", "purple", "b", "brown", "gray"]
num_colors = len(colors)
#cluster assignments:
#a dictionary where cluster_assignments[i] is a list of all points'
#indices whose closest centroid is centroid i
cluster_assignments = {a:[] for a in range(len(x_centroids))}
#The current "stage" of the program that we are currently in
#Either adding "data", adding "centroids", "updating centroids", or "assigning clusters"
stage = "data"

def restart_plot(event):
   """
   Resets the graph's data upon the "Reset" button being clicked.
   """
   global x_points
   global y_points
   global x_centroids
   global y_centroids
   global cluster_assignments
   x_points=[]
   y_points=[]
   x_centroids=[]
   y_centroids=[]
   cluster_assignments = {a:[] for a in range(len(x_centroids))}
   stage="data"
   ax.set_title('Click to add data points') #Initially, the user is adding data points
   ax.set_xlim(0, 10)
   ax.set_ylim(0, 10)
   ax.cla()
   plt.show()

def update_plot(only_data = False):
   """
   Updates the graph visualization.
   """
   ax.cla() #clear the old plot
   ax.set_xlim(0, 10)
   ax.set_ylim(0, 10)
   #Looping over each centroid, draw each centroid and draw each point that is
   #assigned to that centroid in that centroid's color
   if only_data:
      ax.set_title("Click to add data points")
      ax.scatter(x_points, y_points, c="b", marker="o", s=30)
      for i in range(len(x_centroids)):
        ax.set_title("Click to add centroids")
        x = x_centroids[i]
        y = y_centroids[i]
        color = colors[i%num_colors] 
        ax.scatter(x,y,c=color, s = 50, marker="x")
   else:
    # centroids_array = np.array(list(zip(x_centroids,y_centroids))) #each row is a point
    # vor = Voronoi(centroids_array)
    # fig = voronoi_plot_2d(vor,show_vertices=False)
    for i in range(len(x_centroids)):
        x = x_centroids[i]
        y = y_centroids[i]
        color = colors[i%num_colors]
        ax.scatter(x,y,c=color, s = 50, marker="x")
        cluster_points = cluster_assignments[i]
        for p in cluster_points:
          ax.scatter(x_points[p],y_points[p],c=color, marker="o", s=30)
   plt.draw()
      

def assign_clusters():
   """
   Updates the dictionary 'cluster_assignments' where cluster_assignments[i] 
   is a list of all points' indices whose closest centroid is centroid i.
   Returns True if converged, False otherwise
   """
   #each point is assigned to the centroid closest to it
   #points_matrix = np.matrix([x_points, y_points]) #matrix where each column is a data point
   #print(points_matrix)
   #print((len(x_points), len(x_centroids)))
   #cluster_assignments = np.zeros((len(x_points), len(x_centroids)))
   #loop through all data points
   global cluster_assignments
   new_clusters = {a:[] for a in range(len(x_centroids))}
   for i in range (len(x_points)): 
      closest_centroid = 0
      lowest_dist = 20
      #get distance from data point to each centroid
      for j in range (len(x_centroids)): 
         dist_to_centroid = np.linalg.norm((x_points[i]-x_centroids[j], y_points[i]-y_centroids[j]))
         
         if dist_to_centroid < lowest_dist:
            lowest_dist = dist_to_centroid
            closest_centroid = j
      #update point i's closest centroid in cluster_assignments
      #cluster_assignments[i][closest_centroid] = 1
      new_clusters[closest_centroid].append(i)
   #print (cluster_assignments)
   print(new_clusters)
   if new_clusters == cluster_assignments:
      converged = True
   else:
      converged = False
   cluster_assignments = new_clusters
   update_plot()
   return converged

#end result: matrix that has number of centroids columns and number of points rows
#in row i, the jth column will be 1 if ith datapoint should be assigned to jth centroid

def update_centroids():
   """
   Updates x_centroids and y_centroids to be the means of data points 
   assigned to each prior centroid
   """
   global x_centroids
   global y_centroids
   #Initialize lists that are the same lengths as the old centroid lists
   new_x_centroids = [0 for i in range (len(x_centroids))]
   new_y_centroids = [0 for i in range (len(x_centroids))]
   #loop through each cluster
   for (centroid,point_lst) in cluster_assignments.items():
      #Get lists containing all x and y-values of points in that cluster
      all_x = [x_points[i] for i in point_lst]
      all_y = [y_points[i] for i in point_lst]
      #Calculate the mean point of the cluster
      if len(all_x) != 0 and len(all_y) != 0: #only if the cluster has some points
        mean_x = sum(all_x)/len(all_x)
        mean_y = sum(all_y)/len(all_y)
        #Assign this mean as the new centroid
        new_x_centroids[centroid]=(mean_x)
        new_y_centroids[centroid]=(mean_y)
   x_centroids = new_x_centroids
   y_centroids = new_y_centroids
   #Draw the updated centroids on the graph
   update_plot()
   
#for each cluster assigned to a centroid, calculate the mean and store it as the new centroid

# Clicking on the graph will add points
def on_mouse_click(event):
    """
    Add points to the graph where the mouse was clicked.
    Adds data points or initial centroids to the graph,
    depending on the stage of the program the user is in.
    """
    if event.inaxes == ax:
        if stage == "data":
          x_points.append(event.xdata)
          y_points.append(event.ydata)
          #update_points(x_points, y_points, "g")
          update_plot(only_data = True)
        elif stage == "centroids":
           x_centroids.append(event.xdata)
           y_centroids.append(event.ydata)
           #update_points(x_centroids, y_centroids, color="r", marker="x")
           update_plot(only_data = True)

def on_done_button_press(event):
    """
    Proceeds to the next part of the algorithm once the 'Done' button is pressed.
    If data has already been added to the graph, proceeds to place initial centroids.
    If both data and centroids have been added, proceed to assigning clusters.
    """
    global stage
    if stage == "data":
      if not x_points:
         print("Need at least 1 point!")
      else:
        stage = "centroids" #proceed to placing centroids
        ax.set_title("Click to add centroids")
    elif stage == "centroids":
      if not x_centroids:
         print("Need at least 1 centroid!")
      else:
        stage = "assigning clusters" #proceed to assigning clusters 
        ax.set_title("Learning clusters...")
        bdone.label.set_text("Assign Clusters")
    elif stage == "assigning clusters": #proceed to updating centroids
       converged = assign_clusters()
       if converged:
          ax.set_title("Converged!")
       stage = "updating centroids"
       bdone.label.set_text("Update Centroids")
    elif stage == "updating centroids": #proceed to assigning clusters
       update_centroids()
       bdone.label.set_text("Assign Clusters")
       stage = "assigning clusters"
    plt.show()

#Display Done and Reset buttons
ax_button = plt.axes([0.4, 0.05, 0.3, 0.075]) #x0,y0,width,height
bdone = Button(ax_button, "Done")
ax_reset_button=plt.axes([0.1,0.05,0.2,0.075])
breset = Button(ax_reset_button, "Reset")
bdone.on_clicked(on_done_button_press)
breset.on_clicked(restart_plot)

# Connect click event handler
cid = fig.canvas.mpl_connect('button_press_event', on_mouse_click)

plt.show()