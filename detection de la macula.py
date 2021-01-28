
from tkinter import *
import numpy as np
import cv2

from tkinter import filedialog

from PIL import Image 
from PIL import ImageTk

 
class AppUI(Frame):
 
    def __init__(self, master=None):
        Frame.__init__(self, master,relief=SUNKEN,bd=2)
        self.menubar = Menu(self)
        menu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Fichier", menu=menu)
        menu.add_command(label="Ouvrir une image", command=self.ouvrir)
        menu.add_command(label="Enregistrer le resultat", command=self.enregistrer, state='disabled')
        menu.add_command(label="Quitter", command=self.end)
        menu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Traitement", menu=menu)
        menu.add_command(label="Blur", command=self.blur)
        menu.add_command(label="Niveau de gris", command=self.gray)
        menu = Menu(self.menubar, tearoff=0)
      
        self.menubar.add_cascade(label="Macula", menu=menu)
        menu.add_command(label="macula", command=self.macula)
        menu.add_command(label="contour",command=self.contour)
        menu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Originale", menu=menu)
        menu.add_command(label="Image", command=self.initial)
        menu = Menu(self.menubar, tearoff=0)

        self.master.config(menu=self.menubar)
 
        try:
            self.master.config(menu=self.menubar)
        except AttributeError:
            # master is a toplevel window (Python 1.4/Tkinter 1.63)
            self.master.tk.call(master, "config", "-menu", self.menubar)
 
        self.can = Canvas(self, bg="gray", width=300, height=800,
			     bd=0, highlightthickness=0)
        self.can.pack()
        
        topho = 0  # working image de type ImageTk PhotoImage
        img = 0  # input image de type numpy or cv2
        img2 = 0
        height = 0
        width = 0
      
    def end(self):
        import sys
        root.destroy
        sys.exit()
 
    def ouvrir(self):
        # Utilisation d'un dictionnaire pour conserver une rÃ©fÃ©rence
        gifdict={}
        # on efface la zone graphique
        self.can.delete(ALL) #-> AttributeError: 'str' object has no attribute 'tk'
        filename = filedialog.askopenfilename(filetypes=[("Image Files","*.png")])
         
        image = cv2.imread(filename)
        image = cv2.resize(image,(300,300))
        # OpenCV represents images in BGR order; however PIL represents
        # images in RGB order, so we need to swap the channels
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.img = image
        self.img2 = image
        self.height,self.width = (image.shape[0],image.shape[1])
        # convert the images to PIL format...
        self.topho = Image.fromarray(image)
        # ...and then to ImageTk format
        self.topho = ImageTk.PhotoImage(self.topho) # working
        # self.topho = photo

        gifdict[filename] = self.topho  # rÃ©fÃ©rence
        self.can.config(height=image.shape[0],width=image.shape[1])
        self.can.create_image(0,1,anchor=NW,image=self.topho)
        #ligne suivante crÃ©Ã©e car si pas de ligne de commande sur self.can, image apparaÃ®t pas dans canevas
        #self.can.create_title("Image "+str(photo.width())+" x "+str(photo.height()))

    def blur(self): # remove noise
        
        self.img = cv2.GaussianBlur(self.img,(5,5),0)

        blur = Image.fromarray(self.img)
        # ...and then to ImageTk format
        blur = ImageTk.PhotoImage(blur)
        self.topho = blur
        self.can.config(height=self.height,width=self.width)
        self.can.create_image(0,1,anchor=NW,image=self.topho)



    def gray(self):
        #la procedure "ouvrir" a stockÃ© l'image initiale dans self.img en RGB. 
       
        gray = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
        gray = Image.fromarray(gray)
        # ...and then to ImageTk format
        gray = ImageTk.PhotoImage(gray)
        self.topho = gray
        self.can.config(height=self.height,width=self.width)
        self.can.create_image(0,1,anchor=NW,image=self.topho)

    def initial(self):
        photo = Image.fromarray(self.img2)

        # ...and then to ImageTk format
        self.topho = ImageTk.PhotoImage(photo)

        self.can.config(height=self.height,width=self.width)
        self.can.create_image(0,1,anchor=NW,image=self.topho)

 
    def enregistrer(self): print ("enregistrer")
        #la procÃ©dure "ouvrir" a stockÃ© l'image initiale dans self.img en RGB. 
             

 
    def calculer(self): print ("calculer")
 
    def contour (self):  # contour pae filtre de Sobel
       # la procÃ©dure "ouvrir" a stockÃ© l'image initiale dans self.img en RGB. 
                
        gray = cv2.cvtColor(self.img2, cv2.COLOR_BGR2GRAY)
        cnt = cv2.Sobel(gray, cv2.CV_16S, 1, 1)
       # seuillage 
        max = np.max(cnt)
        cnt[cnt <= max/10] = 0
        cnt[cnt > max/10] = 255
        
        photo = Image.fromarray(cnt)

        # pass to ImageTk format
        self.topho = ImageTk.PhotoImage(photo)

        self.can.config(height=self.height,width=self.width)
        self.can.create_image(0,1,anchor=NW,image=self.topho)

    def circle_contour(image):
        # Bounding ellipse
        im = image.copy()
        #easy function
        im = cv2.canny(im, 5,200)
        return im 
     
 
    def macula(self):
        #la procedure "ouvrir" a stockÃ© l'image initiale dans self.img en RGB. 
        # on la recupere dans image 

        image = self.img
        #image = cv2.resize(image,(300,300))   deja resize 300,300 dans ouvrir
        imageCopy = image.copy()
        r,g,b = cv2.split(image) 

        g = cv2.bilateralFilter(g, 5, 17, 17)

        g = g[50:220, 85:220]
         
        blur = cv2.GaussianBlur(g,(31,31),5)
         
        Thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                     cv2.THRESH_BINARY_INV,33,2)


        #applying closing function 

        kernel1 = np.ones((3,3), np.uint8)
        kernel2 = np.ones((3,3), np.uint8)
        disk = cv2.dilate(Thresh, kernel1, iterations=2)
        disk = cv2.erode(disk, kernel2, iterations=1)
        disk = cv2.erode(disk, kernel1, iterations=1)
         
        disk = cv2.GaussianBlur(disk,(5,5),1.5)


        cropm = image[50:220,85:220]

        #find ellipse 

        ff,contours,h = cv2.findContours(disk,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        peri =157.23


        if len(contours) != 0:
          for c in contours:
            arclen = cv2.arcLength(c, True)
            area = cv2.contourArea(c)
            (x,y),r = cv2.minEnclosingCircle(c)
            
            cond = 800<=area<=1500 and len(c)>=5 and 100<arclen<175 and int(y)>50

            if cond:
              cv2.drawContours(cropm,c,-1,(10,0,255),2)
              peri = cv2.arcLength(c, True) #finds the Contour Perimeter
             


        prm = "perimetre (mm) %8.2f"% (peri)
        jaune = (255,255,0)
        font = cv2.FONT_HERSHEY_PLAIN

        cv2.putText(cropm, "Macula", (17, 70), font, 1, jaune)
        cropmB = cv2.resize(cropm,(300,300))
        cv2.putText(cropmB, prm, (2, 15), font, 1, jaune)

        result = np.vstack((imageCopy, cropmB))
        
 
        photo = Image.fromarray(result)

        # ...and then to ImageTk format
        self.topho = ImageTk.PhotoImage(photo)
        self.can.config(height = photo.height,width = photo.width)
        self.can.create_image(0,1,anchor=NW,image=self.topho)
         

#MAIN
root = Tk()
root.geometry("300x800+100+100")  
app = AppUI(root)
app.pack()
 
root.mainloop()
