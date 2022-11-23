import cv2
import time
import numpy as np

class CalibracionHomografia():
    def __init__(self, archivoProyector, imgCamera):        
        self.imgProy = cv2.imread(archivoProyector)
        self.imgCamera = imgCamera.copy()
        self.heightProy, self.widthProy, _ = self.imgProy.shape
        self.areaProy = self.heightProy*self.heightProy
        self.pts = []
        self.ptos_proj =np.array([[0, 0],[0,self.heightProy],[self.widthProy,self.heightProy],[self.widthProy,0]])
    def CrearMascara(self, l_h, l_s, l_v,u_h, u_s, u_v):
        hsv = cv2.cvtColor(self.imgCamera, cv2.COLOR_BGR2HSV)
        l_b = np.array([l_h, l_s, l_v])
        u_b = np.array([u_h, u_s, u_v])
        mask = cv2.inRange(hsv, l_b, u_b)
        #Eliminando ruido
        kernel = np.ones((5,5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        return mask
    def DeteccionBordes(self, mask):
        imgCanny = cv2.Canny(mask, 0, 188)#Canny detector
        #Dilatar para mejorar la visibilidad de los bordes
        #imgDilation = cv2.dilate(imgCanny, kernel, iterations=1)
        #cv2.imshow('dil', imgDilation)
        return imgCanny
    def ObtenerPuntosHomografia(self, bordes, perc, relArea):
        self.pts = []
        time.sleep(1)
        contornos, jerarquia = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        vacio=[0,0];top_left_point=vacio;bottom_left_point=vacio;bottom_right_point=vacio;top_right_point=vacio
        imgContornos=self.imgCamera.copy()
        for i in contornos:
            cv2.drawContours(imgContornos, i,-1,(0,255,0), 2)#-1->Todos los contornos son graficados
            epsilon = perc*cv2.arcLength(i,True)/100.0
            approx = cv2.approxPolyDP(i,epsilon,True) 
            x,y,w,h = cv2.boundingRect(approx)
            area=w*h
            relacion=float(area)*100/self.areaProy
            if len(approx)==4 and relacion>relArea:
                print(approx)
                cent = np.mean(approx, axis=0)
                centx=cent[0][0];centy=cent[0][1]
                #Asignando posiciones del rectangulo
                for [point] in approx:
                    if point[0]<centx and point[1]<centy:
                        top_left_point=[point[0], point[1]]
                    if point[0]<centx and point[1]>centy:
                        bottom_left_point=[point[0], point[1]]
                    if point[0]>centx and point[1]>centy:
                        bottom_right_point=[point[0], point[1]]
                    if point[0]>centx and point[1]<centy:
                        top_right_point=[point[0], point[1]]
                print(top_left_point,bottom_left_point,bottom_right_point,top_right_point)
                
                if (top_left_point!=vacio) & (bottom_left_point!=vacio) & (bottom_right_point!=vacio) & (top_right_point!=vacio):
                    self.pts=np.array([top_left_point,bottom_left_point,bottom_right_point,top_right_point], np.int32)
                    self.pts = self.pts.reshape((-1,1,2))
                    cv2.polylines(imgContornos,[self.pts],True,(255,0,0), 5)
        cv2.imwrite("contorno.png",imgContornos)
        #frameVis=cv2.resize(imgContornos,(1280,1080),interpolation=cv2.INTER_CUBIC)
        cv2.imshow("Imagen deteccion", imgContornos)
        print("fin")
        return self.pts
    def TransformacionHomografica(self, ptos):
        ptos_cam = ptos
        matrix, _ = cv2.findHomography(ptos_cam, self.ptos_proj)
        im_out = cv2.warpPerspective(self.imgCamera, matrix, (self.imgProy.shape[1],self.imgProy.shape[0]))
        #cv2.imshow("Tranformado", im_out)
        
        return matrix
def a(self):
    pass
'''

cv2.namedWindow('ventana')
cv2.createTrackbar('Hmin', 'ventana', 31, 255, a)#117 #120
cv2.createTrackbar('Hmax', 'ventana', 107, 255, a)#130 #16
cv2.createTrackbar('Smin', 'ventana', 47, 255, a)#117 #120
cv2.createTrackbar('Smax', 'ventana', 255, 255, a)#130 #165
cv2.createTrackbar('Vmin', 'ventana', 124, 255, a)#117 #120
cv2.createTrackbar('Vmax', 'ventana', 255, 255, a)#130 #165
cv2.createTrackbar('Percentage', 'ventana', 8, 100, a)#130 #165
cv2.createTrackbar('RelacionArea', 'ventana', 5, 100, a)#130 #165

cap = cv2.VideoCapture(0)

while 1:
    # Sacando un frame
    ret, frame = cap.read()
    cv2.imshow('Imagen', frame)
    
    #Umbrales
    l_h = cv2.getTrackbarPos('Hmin', 'ventana');u_h=cv2.getTrackbarPos('Hmax', 'ventana')
    l_s = cv2.getTrackbarPos('Smin', 'ventana');u_s=cv2.getTrackbarPos('Smax', 'ventana')
    l_v = cv2.getTrackbarPos('Vmin', 'ventana');u_v=cv2.getTrackbarPos('Vmax', 'ventana')
    perc=cv2.getTrackbarPos('Percentage', 'ventana');relArea=cv2.getTrackbarPos('RelacionArea', 'ventana')
    
    calibracion=CalibracionHomografia("proy.png", frame)
    mascara=calibracion.CrearMascara(l_h, l_s, l_v,u_h, u_s, u_v)
    cv2.imshow('Mascara', mascara)

    bordes=calibracion.DeteccionBordes(mascara)
    cv2.imshow('dil', bordes)

    pts=calibracion.ObtenerPuntosHomografia(bordes, perc, relArea)

    if pts!=[]:
        matrixCalibracion=calibracion.TransformacionHomografica(pts)

    k = cv2.waitKey(1) & 0xFF
    if k==ord("q"):
        break
cv2.destroyAllWindows()
'''

