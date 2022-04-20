import maya.cmds as cmds
import re

if(cmds.window("Camera_Plane_Auto_Create", exists = True)):
    cmds.deleteUI("Camera_Plane_Auto_Create")
myWin = cmds.window("Camera_Plane_Auto_Create", title = "Camera ImagePlanes Auto Create", s = True, w = 350, height = 10)
cmds.windowPref( 'Camera_Plane_Auto_Create', remove=True )
cmds.showWindow(myWin)

MainLayout = cmds.columnLayout(adjustableColumn = True)

cmds.text(l = "Created By Charlie Chiao - Non commercial use")

cmds.rowColumnLayout(nr=1)
cmds.text(l = "Select Image Plane Position:")
cmds.separator(w = 18, style = "none")
LeftCheckBox = cmds.checkBox( label= "Left", al = "left", onc = "AddLeftUI()", ofc = "DeleteLeftUI()")
cmds.separator(w = 18, style = "none")
TopCheckBox = cmds.checkBox( label= "Top", al = "left", onc = "AddTopUI()", ofc = "DeleteTopUI()")
cmds.separator(w = 18, style = "none")
FrontCheckBox = cmds.checkBox( label= "Front", al = "left", onc = "AddFrontUI()", ofc = "DeleteFrontUI()")
cmds.setParent(MainLayout)

basicFilter = "*.png ;; *.jpg ;; *.psd ;; *.tiff ;; *.tga"
camList = []
camVal = []



def createCam():
    F = cmds.checkBox(FrontCheckBox, q=True, v= True)
    T = cmds.checkBox(TopCheckBox, q=True, v= True)
    L = cmds.checkBox(LeftCheckBox, q=True, v= True)

    if len(camList)>0:
        for cam in camList:
            cmds.delete(cam)

    if F:
        camN1 = cmds.camera(n="FrontCam")
        cam1 = camN1[1]
        cmds.viewSet(cam1, f = True)
        cmds.camera(cam1, e=True, p=[0,0,50])
        camList.append(cam1)
    if T:
        camN2 = cmds.camera(n="TopCam")
        cam2 = camN2[1]
        cmds.viewSet(cam2, t = True)
        cmds.camera(cam2, e=True, p=[0,50,0])
        camList.append(cam2)
    if L:
        camN3 = cmds.camera(n="LeftCam")
        cam3 = camN3[1]
        cmds.viewSet(cam3, ls = True)
        cmds.camera(cam3, e=True, p=[-50,0,0])
        camList.append(cam3)

    if IsAllImgsSet():
        FImg = cmds.imagePlane(c="%s"%cam1, fn = cmds.textField(FrontImgPlane, q=True, text=True))
        TImg = cmds.imagePlane(c="%s"%cam2, fn = cmds.textField(TopImgPlane, q=True, text=True))
        RImg = cmds.imagePlane(c="%s"%cam3, fn = cmds.textField(LeftImgPlane, q=True, text=True))
 
    if len(camList)>0:
        for cam in camList:
            cmds.hide(cam)
    

def AddLeftUI():
    global LeftPlane
    global LeftImgPlane
    global camVal
    camIndex = "LeftCam"
    camVal.append(camIndex) 
    LeftPlane = cmds.rowColumnLayout(nr = 1, adjustableColumn = True)
    cmds.text(l= "Left Plane")
    cmds.separator(w = 10, style = "none")
    LeftImgPlane = cmds.textField(ed = False, w = 150)
    cmds.separator(w = 10, style = "none")
    ImgSeleteBtn_L = cmds.button(l = "Browse", w = 120, align = "center", c = "BrowseDirectory_L()")
    cmds.setParent(MainLayout)


def DeleteLeftUI():
    cmds.deleteUI(LeftPlane, lay = True)
    camVal.remove("LeftCam")

def AddTopUI():
    global TopPlane
    global TopImgPlane
    global camVal
    camIndex = "TopCam"
    camVal.append(camIndex) 
    TopPlane = cmds.rowColumnLayout(nr = 1, adjustableColumn = True)
    cmds.text(l= "Top Plane")
    cmds.separator(w = 10, style = "none")
    TopImgPlane = cmds.textField(ed = False, w = 150)
    cmds.separator(w = 10, style = "none")
    ImgSeleteBtn_B = cmds.button(l = "Browse", w = 120, align = "center", c = "BrowseDirectory_T()")
    cmds.setParent(MainLayout)

def DeleteTopUI():
    cmds.deleteUI(TopPlane, lay = True)
    camVal.remove("TopCam")

def AddFrontUI():
    global FrontPlane
    global FrontImgPlane
    global camVal
    camIndex = "FrontCam"
    camVal.append(camIndex) 
    FrontPlane = cmds.rowColumnLayout(nr = 1, adjustableColumn = True)
    cmds.text(l= "Front Plane")
    cmds.separator(w = 10, style = "none")
    FrontImgPlane = cmds.textField(ed = False, w = 150)
    cmds.separator(w = 10, style = "none")
    ImgSeleteBtn_F = cmds.button(l = "Browse", w = 120, align = "center", c = "BrowseDirectory_F()")
    cmds.setParent(MainLayout)

def DeleteFrontUI():
    cmds.deleteUI(FrontPlane, lay = True)
    camVal.remove("FrontCam")

def AddApplyBtn():
    ApplyBtn = cmds.button(l = "Apply", w = 120, align = "center", c = "createCam()")
    cmds.setParent(MainLayout)

def BrowseDirectory_T():
    global Img1Set
    checkBoxVal()
    TempFile = cmds.fileDialog2(fm=1, rf=False, ff=basicFilter)
    s = "%s"%TempFile
    result = s[2:-2]
    if len(result)>0:
        cmds.textField(TopImgPlane, e=True, text = "%s"%result)
        Img1Set = True
        if ((FF and Img2Set) and (LL and Img3Set)) or ((FF and Img2Set) and (not LL and not Img3Set)) or ((not FF and not Img2Set) and (LL and Img3Set)) or ((not FF and not Img2Set) and (not LL and not Img3Set)):
            AddApplyBtn()
    else:
        Img1Set = False

def BrowseDirectory_F():
    global Img2Set
    checkBoxVal()
    TempFile = cmds.fileDialog2(fm=1, rf=False, ff=basicFilter)
    s = "%s"%TempFile
    result = s[2:-2]
    if len(result)>0:
        cmds.textField(FrontImgPlane, e=True, text = "%s"%result)
        Img2Set = True
        print(str(TT) + str(Img1Set) + str(LL) + str(Img3Set))
        if ((TT and Img1Set) and (LL and Img3Set)) or ((TT and Img1Set) and (not LL and not Img3Set)) or ((not TT and not Img1Set) and (LL and Img3Set)) or ((not TT and not Img1Set) and (not LL and not Img3Set)):
            AddApplyBtn()
    else:
        Img2Set = False

def BrowseDirectory_L():
    global Img3Set
    checkBoxVal()
    TempFile = cmds.fileDialog2(fm=1, rf=False, ff=basicFilter)
    s = "%s"%TempFile
    result = s[2:-2]
    if len(result)>0:
        cmds.textField(LeftImgPlane, e=True, text = "%s"%result)
        Img3Set = True
        if ((TT and Img1Set) and (FF and Img2Set)) or ((TT and Img1Set) and (not FF and not Img2Set)) or ((not TT and not Img1Set) and (FF and Img2Set)) or ((not TT and not Img1Set) and (not FF and not Img2Set)):
            AddApplyBtn()
    else:
        Img3Set = False

def IsAllImgsSet():
    F = cmds.checkBox(FrontCheckBox, q=True, v= True)
    T = cmds.checkBox(TopCheckBox, q=True, v= True)
    L = cmds.checkBox(LeftCheckBox, q=True, v= True)

    if F == False and T == False and L == False:
        return False
    else:
        if (F and cmds.textField(FrontImgPlane, q=True, text=True) == "") or (T and cmds.textField(TopImgPlane, q=True, text=True) == "") or (L and cmds.textField(LeftImgPlane, q=True, text=True) == ""):
            return False
        else:
            return True

def ImgSet():
    global Img1Set
    Img1Set = False
    global Img2Set
    Img2Set = False
    global Img3Set
    Img3Set = False

def checkBoxVal():
    global FF
    global TT
    global LL
    FF = cmds.checkBox(FrontCheckBox, q=True, v= True)
    TT = cmds.checkBox(TopCheckBox, q=True, v= True)
    LL = cmds.checkBox(LeftCheckBox, q=True, v= True)

ImgSet()