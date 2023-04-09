import base64

class myImage():

    def bytesToImage(bytes):
        img =base64.b64decode(bytes)
        with open("tmp.png" ,'wb') as fp:
            fp.write(img)