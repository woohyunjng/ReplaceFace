from random import choice
from string import ascii_letters
from os import listdir

from cv2 import imdecode, cvtColor, CascadeClassifier, COLOR_BGR2RGB, IMREAD_COLOR
from cv2.data import haarcascades

from PIL.Image import fromarray, open

from numpy import fromfile, uint8


INP = "./input/"
OUT = "./output/"


def gen_filename():
    while True:
        a = "".join([choice(ascii_letters) for _ in range(16)]) + ".png"
        if a not in listdir(OUT):
            return a


face = INP + input("바꿀 얼굴의 파일명을 알려주세요: ")
image = INP + input("사진의 파일명을 알려주세요: ")
if face.split(".")[-1] not in ["png", "jpg", "jpeg"] or image.split(".")[-1] not in [
    "png",
    "jpg",
    "jpeg",
]:
    print("파일의 형식이 올바르지 않습니다")
    exit()

scale = input("스케일을 입력해주세요(무입력시 1.3): ")
try:
    scale = float(scale) if scale else 1.3
except:
    print("스케일의 형식이 올바르지 않습니다")
    exit()

try:
    cv2_image = cvtColor(imdecode(fromfile(image, uint8), IMREAD_COLOR), COLOR_BGR2RGB)
    pillow_image = fromarray(cv2_image)

    faces = CascadeClassifier(
        haarcascades + "haarcascade_frontalface_default.xml"
    ).detectMultiScale(cv2_image, scaleFactor=scale, minNeighbors=3, minSize=(30, 30))
    if not len(faces):
        print("사진에 얼굴이 발견되지 않았습니다")
        exit()

    for x, y, w, h in faces:
        pillow_image.paste(open(face).resize((w, h)), (x, y))

    name = f"{OUT}{gen_filename()}"
    pillow_image.save(name)

    print(f"{name}에 저장되었습니다")
except:
    print("모종의 오류가 발생했네요")
