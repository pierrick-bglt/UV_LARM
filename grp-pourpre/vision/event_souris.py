import cv2
import numpy as np

def souris(event, x, y, flags, param):
    global lo, hi, color, hsv_px
    
    if event == cv2.EVENT_MOUSEMOVE:
        # Conversion des trois couleurs RGB sous la souris en HSV
        px = frame[y,x] # inversé car convention 
        px_array = np.uint8([[px]]) # création image 
        hsv_px = cv2.cvtColor(px_array,cv2.COLOR_BGR2HSV)
    
    if event==cv2.EVENT_MBUTTONDBLCLK:
        color=image[y, x][0]

    if event==cv2.EVENT_LBUTTONDOWN:
        if color>5:
            color-=1

    if event==cv2.EVENT_RBUTTONDOWN:
        if color<250:
            color+=1
            
    lo[0]=color-5   # intervalle d'erreur 
    hi[0]=color+5

color=100 # teinte de départ

lo=np.array([color-5, 100, 50]) # H S V 
hi=np.array([color+5, 255,255])

color_info=(0, 0, 255)

cap=cv2.VideoCapture(0)
cv2.namedWindow('Camera')
cv2.setMouseCallback('Camera', souris)
hsv_px = [0,0,0]

while True: # permets la lecture en continue 
    ret, frame=cap.read() #lecture d'une image # ret booléen 
    image=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convertis en HSV
    mask=cv2.inRange(image, lo, hi) # fonction qui filtre en blanc tous les pixels entre lo et hi de l'image # double seuillage 
    #image=cv2.blur(image, (7, 7)) # permets de flouter l'image 
    #mask=cv2.erode(mask, None, iterations=4) # filtre le bruit en diminuant la taille des pixels
    #mask=cv2.dilate(mask, None, iterations=4) # augmente la taille des pixels de la zone blanche 
    image2=cv2.bitwise_and(frame, frame, mask= mask) # permets d'afficher l'image segmenté avec un et logique 
    cv2.putText(frame, "Couleur: {:d}".format(color), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, color_info, 1, cv2.LINE_AA)
    
    # Affichage des composantes HSV sous la souris sur l'image
    pixel_hsv = " ".join(str(values) for values in hsv_px)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, "px HSV: "+pixel_hsv, (10, 260),
               font, 1, (255, 255, 255), 1, cv2.LINE_AA)
               
    cv2.imshow('Camera', frame)
    cv2.imshow('image2', image2)
    cv2.imshow('Mask', mask)
    
    if cv2.waitKey(1)&0xFF==ord('q'): # récupère la touche qui a été appuyé, waitkey en mini seconde
        break


cap.release()   # libère la webcam 
cv2.destroyAllWindows()