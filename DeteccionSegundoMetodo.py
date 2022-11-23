import cv2
import time
import numpy as np

class DeteccionSegundoMetodo():
    def __init__(self, im):        
        self.img = im.copy()
        self.coordenadaX=None;self.coordenadaY=None
        
    def CrearMascara(self, l_h, l_s, l_v,u_h, u_s, u_v):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(hsv, l_b, u_b)
        kernal = np.ones((5, 5), "uint8")
        mask = cv2.dilate(mask, kernal)
        return mask
    def EncontrarPuntoDisparo(self, mask, l_a):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        frame=self.img.copy()
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > l_a:
                (self.coordenadaX, self.coordenadaY), radius = cv2.minEnclosingCircle(contour)
                center = (int(self.coordenadaX), int(self.coordenadaY))
                frame = cv2.circle(frame, center, 10, (0, 200, 10), 2)
        cv2.imwrite("deteccion.png",frame)  
        #frameVis=cv2.resize(frame,(1280,1080),interpolation=cv2.INTER_CUBIC)
        #cv2.imshow("Imagen deteccion", frame)
            
        return self.coordenadaX,self.coordenadaY,frame
def a(self):
    pass
'''
cv2.namedWindow('ventana')
cv2.createTrackbar('Hmin', 'ventana', 32, 255, a)#117 #120
cv2.createTrackbar('Hmax', 'ventana', 174, 255, a)#130 #165
cv2.createTrackbar('Smin', 'ventana', 105, 255, a)#117 #120
cv2.createTrackbar('Smax', 'ventana', 169, 255, a)#130 #165
cv2.createTrackbar('Vmin', 'ventana', 90, 255, a)#117 #120
cv2.createTrackbar('Vmax', 'ventana', 255, 255, a)#130 #165
cv2.createTrackbar('Amin', 'ventana', 49, 255, a)#130 #165

cap = cv2.VideoCapture(0)
while 1:
    # Sacando un frame
    ret, frame = cap.read()

    #Umbrales
    l_h = cv2.getTrackbarPos('Hmin', 'ventana');u_h=cv2.getTrackbarPos('Hmax', 'ventana')
    l_s = cv2.getTrackbarPos('Smin', 'ventana');u_s=cv2.getTrackbarPos('Smax', 'ventana')
    l_v = cv2.getTrackbarPos('Vmin', 'ventana');u_v=cv2.getTrackbarPos('Vmax', 'ventana')
    l_a = cv2.getTrackbarPos('Amin', 'ventana')/10.0

    detect=DeteccionSegundoMetodo(frame)
    mascara=detect.CrearMascara(l_h, l_s, l_v,u_h, u_s, u_v)
    
    CoordenadaX, CoordenadaY, frame=detect.EncontrarPuntoDisparo(mascara, l_a) 

    if (CoordenadaX is not None) and (CoordenadaX is not None):
        print(CoordenadaX, CoordenadaY) 
    
    k = cv2.waitKey(1) & 0xFF
    if k==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
'''
        
