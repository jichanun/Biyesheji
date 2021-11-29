import cv2
import numpy as np 
import time
import matplotlib.pyplot as plt

#cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX
font1 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 23,
         }
img = np.zeros((1024,1024,3),np.uint8)
cv2.line(img,(0,0),(511,511),(255,0,0),10)
#cv2.circle(img2,(255,255),127,(0,0,255),-1)
def ChangeCircle (img2,center):
    cv2.circle(img2,(center,center),20,(0,255,0),-1)
    cv2.putText (img2, "a= %d"%center,(center-30,center+50),font,1,(255,255,255),2)
center =0
'''
while cv2.waitKey(1) != 27:
    img2 =  np.zeros((512,512,3),np.uint8)
    ChangeCircle(img2,center)
    cv2.imshow ("line",img)
    cv2.imshow ("circles",img2)
    center+=1
    time.sleep(0.1)
'''
x = 255
y =  255

plt.show()
figsizee= 10,10
plt.figure(figsize= (10,10))
for i in range (50):
        img2 =  np.zeros((1024,1024,3),np.uint8)
        #img2.fill(255)
        ChangeCircle(img2,center)
        
        plt.imshow(img2)
        #plt.plot(x,y,"ob",c='g') 
        plt.title("All The Robot's Position \n\n",font1) 
        plt.title("Green : Friends,Red :Target, Blue :Expect",loc='left') 
        plt.xlabel("x axis caption",font1) 
        plt.ylabel("y axis caption",font1) 
        plt.tick_params(labelsize=23)
        plt.yticks([1000,800,600,400,200,0],[0,2,4,6,8,10])
        plt.xticks([0,200,400,600,800,1000],[0,2,4,6,8,10])
        #plt.show(block = False)
        #plt.gca().invert_yaxis()
        plt.pause(0.001)
        plt.clf()
        #time.sleep(0.1)
        x+=2
        y+=2
        center +=2
        print(i)



