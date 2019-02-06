import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import imageio

def plotLine(line):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = line.intercept + line.slope * x_vals
    plt.plot(x_vals, y_vals, '--')
    
def verticalDistance(point, line):
    # Returns the vertical distance from the line to the point
    lineHeight = point[0] * line.slope + line.intercept
    pointHeight = point[1]
    
    return pointHeight - lineHeight
    
class Line:
    def __init__(self, slope = 0, intercept = 1):
        self.slope = slope
        self.intercept = intercept
        
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y =y
        
class Regressor:
    def __init__(self, line, points, epochs, learningRate):
        self.line = line
        self.points = points
        self.epochs = epochs
        self.learningRate = learningRate

    # Calculates the line of best fit for the given points
    def regress(self):
        for i in range(1, 2):
            # Pick a random point
            point = random.choice(self.points)
            v = verticalDistance(point, self.line) # The vertical distance from the line to the point
            h = point[0] # The horizontal distance from the point to the y axis
            
            # Adjust slope
            self.line.slope += v * h * self.learningRate
            
            # Adjust intercept
            self.line.intercept += v * self.learningRate
            
            # Output current mean square error
            #if i % 10 == 0:
                #print('MSE: ' + str(self.mse()))
                #print('AE: ' + str(self.ae()))
            
    # Returns the mean squared error for the current line and points
    def mse(self):
        error = 0
        for point in points:
            error += verticalDistance(point, self.line) ** 2
        
        return error / len(points)
    
    # Returns the absolute error for the current line and points
    def ae(self):
        error = 0
        for point in points:
            error += verticalDistance(point, self.line)
        
        return error
        
    # Plots the graph and returns it as an image
    def getImage(self):
        axis = plt.gca()
        axis.set_xlim([-5, 5])
        axis.set_ylim([-5, 5])
        figure = plt.figure()
        figure.clear()
        
        #xx = [item for sublist in x for item in sublist]
        #yy = [item for sublist in y for item in sublist]
        
        # Show horizontal and vertical lines
        plt.axhline(0, color='r', zorder=-1)
        plt.axvline(0, color='r', zorder=-1)
        
        # Plot points and line of best fit
        plt.scatter(x, y)
        plotLine(line)
        
        axis.set_ylim(0, 10)
        figure.canvas.draw()
        
        image = np.frombuffer(figure.canvas.tostring_rgb(), dtype='uint8')
        image  = image.reshape(figure.canvas.get_width_height()[::-1] + (3,))

        return image
        
        
# Start with y = -2x + 3
line = Line(-2, + 4)

# Create our points
totalPoints = 100
x = np.random.randn(totalPoints, 1) + 0.5
y = x * 1.2 + np.random.randn(totalPoints, 1) * 2.6 + 1
points = list(zip(x, y))

# Create the regressor
epochs = 1000
learningRate = 0.005
regressor = Regressor(line, points, epochs, learningRate)

def saveImage():
    regressor.regress()
    return regressor.getImage()
    
# Save as a gif
kwargs_write = {'fps':60.0, 'quantizer':'nq'}
imageio.mimsave('./powers.gif', [saveImage() for i in range(epochs)], fps=60)
