from DeteccionSegundoMetodo import DeteccionSegundoMetodo
from CalibracionHomografia import CalibracionHomografia
import cv2
import time
import numpy as np

def calibrar():
    cap = cv2.VideoCapture(0)
    while 1:
    # Sacando un frame
        ret, frame = cap.read()
        cv2.imshow('Imagen', frame)
        
        #Umbrales
        l_h = 31; u_h=107
        l_s = 47; u_s=255
        l_v = 124; u_v=255
        perc= 8; relArea=5
        
        calibracion=CalibracionHomografia("proy.png", frame)
        mascara=calibracion.CrearMascara(l_h, l_s, l_v,u_h, u_s, u_v)
        cv2.imshow('Mascara', mascara)

        bordes=calibracion.DeteccionBordes(mascara)
        cv2.imshow('dil', bordes)

        pts=calibracion.ObtenerPuntosHomografia(bordes, perc, relArea)

        if pts!=[]:
            matrixCalibracion=calibracion.TransformacionHomografica(pts)
            print("listo")
            break
           
        k = cv2.waitKey(1) & 0xFF
        if k==ord("q"):
            break
    return matrixCalibracion
    
def encontrarPunto():
    cap = cv2.VideoCapture(0)

    while 1:
        # Sacando un frame
        ret, frame = cap.read()

        #Umbrales
        l_h = 32;u_h=174
        l_s = 105;u_s=169
        l_v = 90;u_v=255
        l_a = 49

        detect=DeteccionSegundoMetodo(frame)
        mascara=detect.CrearMascara(l_h, l_s, l_v,u_h, u_s, u_v)
        
        CoordenadaX, CoordenadaY, frame=detect.EncontrarPuntoDisparo(mascara, l_a) 

        if (CoordenadaX is not None) and (CoordenadaX is not None):
            print(CoordenadaX, CoordenadaY) 
            break
        k = cv2.waitKey(1) & 0xFF
        if k==ord("q"):
            break
    return CoordenadaX, CoordenadaY, frame
    
def obtenerPuntoProyectado(matriz, imgCamara, CoordenadaX, CoordenadaY):
    imgProy=cv2.imread("proy.png")
    im_out = cv2.warpPerspective(imgCamara, matriz, (imgProy.shape[1],imgProy.shape[0]))
    #pProy=cv2.perspectiveTransform(np.float32([CoordenadaX, CoordenadaY]), matriz)
    p = np.array((CoordenadaX,CoordenadaY,1)).reshape((3,1))
    temp_p = matriz.dot(p)
    sum = np.sum(temp_p ,1)
    px = int(round(sum[0]/sum[2]))
    py = int(round(sum[1]/sum[2]))
    pProy=[px,py]
    cv2.imwrite('Proyeccion.png',im_out)
    print(pProy)
    return pProy, im_out
        
#Calibrando
matrizCalibracion=calibrar()
time.sleep(3)
CoordenadaX, CoordenadaY, imgDeteccion=encontrarPunto()
CoordenadaProy, imgTransformada=obtenerPuntoProyectado(matrizCalibracion, imgDeteccion, CoordenadaX, CoordenadaY)



