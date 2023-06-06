from imgutils import *
from PIL import ImageDraw, Image
import pytesseract
import re
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class imageToRead:

    def __init__(self, name):

        self.imageObject = cv2.imread('data/' + name)
        self.originalImage = self.imageObject

    def ResizeImage(self, ratio):
        self.imageObject = opencv_resize(self.imageObject, ratio / self.imageObject.shape[0])

    def Rgb2Gray(self):
        self.imageObject = cv2.cvtColor(self.imageObject, cv2.COLOR_BGR2GRAY)

    def BlurImage(self, taille, sigma):
        self.imageObject = cv2.GaussianBlur(self.imageObject, (taille, taille), sigma)

    def DilateImage(self, taille):
        noyau = cv2.getStructuringElement(cv2.MORPH_RECT, (taille, taille))
        self.imageObject = cv2.dilate(self.imageObject, noyau)

    def CropOnEdge(self, seuil, aperSize, plotDraw1, plotDraw2, plotDraw3):
        canny = cv2.Canny(self.imageObject, seuil, seuil+100, apertureSize=aperSize)
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
        sorted_contours = sorted_contours[:10]

        ticket_contours = get_receipt_contour(sorted_contours)

        if plotDraw1:
            draw = cv2.drawContours(self.originalImage.copy(), contours, -1, (0, 255, 0), 3)
            plot_rgb(draw)

        if plotDraw2:
            draw2 = cv2.drawContours(self.originalImage.copy(), sorted_contours, -1, (0, 255, 0), 3)
            plot_rgb(draw2)

        if plotDraw3:
            draw3 = cv2.drawContours(self.originalImage.copy(), ticket_contours, -1, (0, 0, 255), 3)
            plot_rgb(draw3)

        contour_area = cv2.contourArea(ticket_contours)
        image_area = self.imageObject.shape[0] * self.imageObject.shape[1]

        ratio = contour_area / image_area
        #print(ratio)

        if ratio < 0.1:
            return 0

        tab = contour_to_rect(ticket_contours, ratio)
        im_per = wrap_perspective(self.originalImage.copy(), tab)
        im_per = bw_scanner(im_per)
        #plot_gray(im_per)
        self.imageObject = im_per

    def ExtractText(self, showExtractedText):
        Texte = pytesseract.image_to_string(self.imageObject)

        if showExtractedText:
            data = pytesseract.image_to_data(self.imageObject, output_type=pytesseract.Output.DICT)
            image = Image.fromarray(self.imageObject)
            for i in range(len(data['text'])):
                # Récupération des coordonnées
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

                # Dessin d'un rectangle autour du texte
                draw = ImageDraw.Draw(image)
                draw.rectangle((x, y, x + w, y + h), outline="red", width=2)
            image.show()

        return Texte

    def ExtractBiggerText(self):

        Text = pytesseract.image_to_string(self.imageObject)

        words = Text.split()

        word_sizes = [(word, cv2.getTextSize(word, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0][0]) for word in words]

        sorted_words = sorted(word_sizes, key=lambda x: x[1], reverse=True)

        sorted_words = [word[0] for word in sorted_words]

        pattern = r'^[0-9]+(?:[.,][0-9]+)?$'

        return [w for w in sorted_words if re.match(pattern, w)]


    def SplitImage(self, showResult = False):

        image = self.imageObject

        # Récupérer la hauteur et la largeur de l'image
        height, width = image.shape[:2]

        # Diviser l'image en deux moitiés égales
        half_height = height // 2
        top_half = image[:half_height, :]
        bottom_half = image[half_height:, :]

        if showResult:
            plt.imshow(bottom_half)
            plt.show()

        self.imageObject = bottom_half

    def AddVerticalStripes(self, showResult = False):
        band_width = 50
        band_height = self.imageObject.shape[0]

        left_band = np.full((band_height, band_width, 3), (42, 42, 165), dtype=np.uint8)
        left_band = cv2.cvtColor(left_band, cv2.COLOR_BGR2GRAY)
        right_band = np.full((band_height, band_width, 3), (42, 42, 165), dtype=np.uint8)
        right_band = cv2.cvtColor(right_band, cv2.COLOR_BGR2GRAY)

        img_with_bands = np.concatenate((left_band, self.imageObject, right_band), axis=1)
        self.imageObject = img_with_bands

        if showResult:
            cv2.imshow('Image with stripes', img_with_bands)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def AddHorizontalStripes(self, showResult = False):
        band_width = self.imageObject.shape[1]
        band_height = 50

        top_band = np.full((band_height, band_width, 3), (42, 42, 165), dtype=np.uint8)
        top_band = cv2.cvtColor(top_band, cv2.COLOR_BGR2GRAY)
        bottom_band = np.full((band_height, band_width, 3), (42, 42, 165), dtype=np.uint8)
        bottom_band = cv2.cvtColor(bottom_band, cv2.COLOR_BGR2GRAY)

        img_with_bands = np.concatenate((top_band, self.imageObject, bottom_band), axis=0)

        self.imageObject = img_with_bands

        if showResult:
            cv2.imshow('Image with stripes', img_with_bands)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def extract_text_with_rotation(self):
        # Charger l'image en niveaux de gris
        picture = self.imageObject
        # Appliquer une détection de contours
        edges = cv2.Canny(picture, 50, 150, apertureSize=3)

        # Rechercher les lignes dans l'image
        lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

        # Calculer l'angle moyen des lignes détectées
        angles = []
        for line in lines:
            rho, theta = line[0]
            angle = np.degrees(theta)
            angles.append(angle)
        mean_angle = np.mean(angles)

        # Rotation de l'image pour corriger l'inclinaison du texte
        rotated_image = rotate_image(picture, -mean_angle)

        # Utiliser pytesseract pour extraire le texte de l'image corrigée
        extracted_text = pytesseract.image_to_string(rotated_image)

        return extracted_text

def rotate_image(pic, angle):
    height, width = pic.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    rotated_image = cv2.warpAffine(pic, rotation_matrix, (width, height))
    return rotated_image
