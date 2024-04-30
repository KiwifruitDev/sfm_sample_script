# SFM Sample Script
# A template for creating a main menu script for Source Filmmaker.
# https://github.com/KiwifruitDev/sfm_sample_script
# This software is licensed under the MIT License.
# Copyright (c) 2024 KiwifruitDev

import sfm
from vs import movieobjects
import sfmApp
from PySide import QtGui, QtCore, shiboken

try:
    sfm
except NameError:
    from sfm_runtime_builtins import *

ProductName = "Sample"
InternalName = "sample"

class ScriptWindow(QtGui.QWidget):
    def __init__(self):
        super( ScriptWindow, self ).__init__()
        ShowMessageBox("Hello World!", Information)
        self.initUI()
    def initUI(self):
        layout = QtGui.QVBoxLayout()
        label = QtGui.QLabel("Hello World!")
        layout.addWidget(label)
        self.setLayout(layout)

NoIcon = QtGui.QMessageBox.NoIcon
Question = QtGui.QMessageBox.Question
Information = QtGui.QMessageBox.Information
Warning = QtGui.QMessageBox.Warning
Critical = QtGui.QMessageBox.Critical

def ShowMessageBox(message, icon=Information):
    msgBox = QtGui.QMessageBox()
    msgBox.setText(message)
    msgBox.setIcon(icon)
    title = ProductName
    if icon == Question:
        title = title + ": Question"
    elif icon == Warning:
        title = title + ": Warning"
    elif icon == Critical:
        title = title + ": Error"
    else:
        title = title + ": Information"
    msgBox.setWindowTitle(title)
    msgBox.exec_()

def CreateScriptWindow():
    try:
        scriptWindow = ScriptWindow()
        globals()[InternalName + "_window"] = scriptWindow
        pointer = shiboken.getCppPointer(scriptWindow)
        sfmApp.RegisterTabWindow(InternalName + "_window", ProductName, pointer[0] )
    except Exception as e:
        import traceback
        traceback.print_exc()        
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Error: %s" % e)
        msgBox.exec_()

def DestroyScriptWindow():
    try:
        globalScriptWindow = globals().get(InternalName + "_window")
        if globalScriptWindow is not None:
            globalScriptWindow.close()
            globalScriptWindow.deleteLater()
            globalScriptWindow = None
            globals()[InternalName + "_window"] = None
    except Exception as e:
        import traceback
        traceback.print_exc()        
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Error: %s" % e)
        msgBox.exec_()

try:
    # Create window if it doesn't exist
    globalScriptWindow = globals().get(InternalName + "_window")
    if globalScriptWindow is None:
        CreateScriptWindow()
    else:
        dialog = QtGui.QMessageBox.warning(None, ProductName + ": Error", ProductName + " is already open.\n\nIf you are a developer, click Yes to forcibly open a new instance.\n\nOtherwise, click No to close this message.", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        if dialog == QtGui.QMessageBox.Yes:
            DestroyScriptWindow()
            CreateScriptWindow()
    try:
        sfmApp.ShowTabWindow(InternalName + "_window")
    except:
        pass
except Exception  as e:
    import traceback
    traceback.print_exc()        
    ShowMessageBox("Error: %s" % e, Critical)

if InternalName + "_ran" not in globals():
    globals()[InternalName + "_ran"] = True
