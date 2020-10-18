import cv2
import numpy as np

colors = ['Green', 'Blue' , 'Orange' , 'Yellow']
colorsMinMax = np .array([
    [[25, 52 , 72],
    [102 ,255 ,255]],
    [[94,80,2],
    [126,255,255]],
    [[0,100,100],
    [18 ,255 ,255]],
    [[20,100,100],
    [40,255,255]]]
)
window = 'Segmentation'
window2 = 'HSV'
buttons = np.zeros  (len(colors))#All are 0 at beginning
types = ["Hue" , "Saturation" , "Value"]

def adjustTrackBars(index):
    arr = colorsMinMax[index]
    for  i in range(len(types)):
        cv2.setTrackbarMin(types[i],window2,0)
        cv2.setTrackbarMax(types[i],window2,arr[1 ,i])
        cv2.setTrackbarPos(types[i] , window2 , arr[0,i])

def changeTracks(value):
    for i in range (len(buttons)):
        value = cv2.getTrackbarPos(colors[i] , window)
        if value != buttons[i]:#All other values must be set to false
            if value == 1:
                adjustTrackBars(i)#Adjust track bars in other window
                buttons[buttons != i] = 0
                buttons[i] = 1
                for j in colors:
                    if j!=colors[i]:
                        cv2.setTrackbarPos(j,window , 0)
                break
            else:#Value == 0 reset
                for i in types:
                    cv2.setTrackbarMin(i,window2,0)
                    cv2.setTrackbarMax(i,window2,0)
                    cv2.setTrackbarPos(i , window2 ,0)
                    buttons[:] = 0
           
                
def getTrackBarResults(hsvCol):
    color = -1
    for i in range(len(buttons)):
        if buttons[i] == 1:
            color = i
            break
    if color == -1:#No Segmentation
        return False,0
    #Now we get the upper and lower boundaries
    #Higher bounds are constant , trackbars changes lower bounds
    lowerBounds = np.array([cv2.getTrackbarPos(types[i],window2) for i in range(3)])
    upperBounds = colorsMinMax[color,1]
    mask = cv2.inRange(hsvCol , lowerBounds , upperBounds)
    return True,mask
    
    
        
def none(value):
    pass                    


cap = cv2.VideoCapture(0)
cv2.namedWindow(window)
cv2.resizeWindow(window , 300 , 200)
cv2.namedWindow(window2)
cv2.resizeWindow(window2 , 300 , 200)
for i in colors:
    cv2.createTrackbar(i,window , 0 ,1,changeTracks)
for i in types:
    cv2.createTrackbar(i,window2 , 0, 0,none)   
while True:
    _,frame = cap.read()
    hsvCol = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
    ret,mask = getTrackBarResults(hsvCol)
    if ret:
        new  = cv2.bitwise_and(frame , frame , mask = mask)
        cv2.imshow("Segment" , new)
    else:
        cv2.destroyWindow('Segment')    
    cv2.imshow("Image" , frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()        
cv2.destroyAllWindows()        
