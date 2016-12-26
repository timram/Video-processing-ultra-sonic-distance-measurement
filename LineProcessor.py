"""
This module desribe class that process vectors of incoming lines
and returns couple of coordinates of x axes of left and right line
"""
import numpy as np

class LineProcessor():
    def ProcessLines(self, lines):
        verticalLines = []
        leftLines = []
        rightLines = []
        sumLeft = 0
        sumRight = 0
        leftMiddle = 0
        rightMiddle = 0
        
        for coord in lines:
            angle = np.arctan2(coord[3] - coord[1], coord[2]- coord[0]) * 180. / np.pi
            if np.abs(angle) > 20:
                verticalLines.append(coord)
    
        verticalLines = np.array(verticalLines)

        if verticalLines.size == 0:
            return
        
        for tmpLine in verticalLines:
            if (tmpLine[0] > 420):
                rightLines.append(tmpLine[0::2])
            elif (tmpLine[2] < 380):
                leftLines.append(tmpLine[0::2])
    
        leftLines = np.array(leftLines)
        rightLines = np.array(rightLines)
        
        if leftLines.size == 0 and rightLines.size == 0:
            return
        
        if leftLines.size > 0:
            for value in leftLines:
                sumLeft += np.sum(value)
            leftMiddle = sumLeft / leftLines.size

        if rightLines.size > 0:
            for value in rightLines:
                sumRight += np.sum(value)
            rightMiddle = sumRight / rightLines.size

        return [leftMiddle, rightMiddle]