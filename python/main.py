import imageToRead
import re
import itertools

ResizeParam = [800, 1000, 1300]
BlurParam = [3, 5, 7]
DilateParam = [3, 5, 7]
CropParam = [50, 100]
Totals = []

def main(value):

    for params in itertools.product(ResizeParam, BlurParam, DilateParam, CropParam):
        Resize, Blur, Dilate, Crop = params
        try:
            ReceiptPicture = imageToRead.imageToRead(str(value)+'-receipt.jpg')
            ReceiptPicture.SplitImage()
            ReceiptPicture.ResizeImage(Resize)
        except:
            print("erreur sur le " + str(value) + "-receipt.jpg")
            break
        ReceiptPicture.Rgb2Gray()
        ReceiptPicture.BlurImage(Blur, 0)
        ReceiptPicture.DilateImage(Dilate)

        try:
            ReceiptPicture.CropOnEdge(Crop, 5, False, False, False)
        except:
            pass

        Texte = ReceiptPicture.ExtractText(False)
        Numbers = GetNumbers(Texte)
        Total = TotalEstimator(Numbers)

        Totals.append(Total)

    print(Totals)


    #print(Occurence(Totals))
    if len(Totals) != 0:
        if type(Occurence(Totals)[0]) == float or len(Occurence(Totals)) == 1:
            print(str(value) + " : " + str(Occurence(Totals)[0]))
        else:
            print(str(value) + " : " + str(Occurence(Totals)[1]))

def GetNumbers(text):
    regex = r'\d+\.\d+'
    regex2 = r'\d+\,\d+'
    nombres = re.findall(regex, text)
    nombres2 = re.findall(regex2, text)
    nombres = [float(nombre) for nombre in nombres]
    nombres2 = [float(nombre.replace(',','.')) for nombre in nombres2]
    output = nombres + nombres2
    new_output = []
    for nombre in output:

        if isinstance(nombre, float) and nombre == round(nombre, 2):
            new_output.append(nombre)
        else:
            continue

    return new_output

def TotalEstimator(Numbers):
    Numbers.sort(reverse = True)
    for number in Numbers:
        if number < 1000:
            return number

def Occurence(list):
    dict_occurrence = {}
    for i in list:
        if i not in dict_occurrence:
            dict_occurrence[i] = 1
        else:
            dict_occurrence[i] += 1
    return sorted(dict_occurrence, key=dict_occurrence.get, reverse=True)



for i in range(1133, 1134, 1):
    main(i)
    Totals = []
