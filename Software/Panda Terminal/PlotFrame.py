#----------------------------------------------------------------------

# Software da PANDA
# TCC - Engenharia Mecatrônica - Poli USP
# Guilherme de Agrela Lopes
# João Vitor Sanches
#
# PLOT FRAME
#
# Arquivos:
# MainFrame: Tela principal; chamada das outras classes
# CalibrationFrame: Tela para realizar a calibração da placa; criada ao clicar no botão 'Modo de Calibração' da tela principal
# PlotFrame: Telas com os gráficos gerados a partir das seleções na tela de Configuração; criadas ao clicar no botão 'Mostrar Gráficos'
# SettingsFrame: Tela para escolher as configurações desejadas do programa; criada ao clicar no botão 'Configurações'
# PandaDialogs: Diálogos de erro relacionados com a PANDA
# panda_board: Interação do software com o firmware da PANDA

#----------------------------------------------------------------------

import wx

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
from matplotlib import pyplot as plt

from time import time

from panda_board import panda

import os

import numpy as np

import PandaDialogs
from PandaDialogs import myPanda

# Globals
looped = False
start = time()


class PlotFrame(wx.Frame):
    """
    This is the Plot Frame.  It plots in real time the graphics that the user has chosen 
    in the Settings Frame.  The user has the option to save the plot as an image or
    save the data in .csv format.
    """
    def __init__(self, chooseUnit, Ks, Kf, Kt, Kp, parent, title):
        self.dpi = 100
        self.height = 5
        self.width = 10

        wx.Frame.__init__(self, parent, -1, title,
                            pos=((self.width * self.dpi)-500, (self.height * self.dpi)-300), size=(1000,600))

        # Initializes unit and constants
        self.unit = chooseUnit
        self.Ks = Ks
        self.Kf = Kf
        self.Kt = Kt
        self.Kp = Kp

        # Defines maximum sizes
        self.maximumData = 5
        self.maximumArray = 3000

        # Gets initial value from function in PandaDialogs
        initialValue = PandaDialogs.dataConversion(self.unit, self.Ks, self.Kf, self.Kt, self.Kp)

        self.avgOver = 50

        self.data = [initialValue]
        self.time = [0]
        self.avgData = [initialValue]

        self.totalTime = 0

        self.fileTime = [0]
        self.fileValue = [initialValue]
        self.fileAvg = [initialValue]

        self.panel = wx.Panel(self, -1)

        self.initPlot()
        self.createMenu()

        self.canvas = FigCanvas(self.panel, -1, self.fig)

        # Creates timers
        self.redrawTimer = wx.Timer(self)
        self.updateValueTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onRedrawTimer, self.redrawTimer)
        self.Bind(wx.EVT_TIMER, self.updateValue, self.updateValueTimer)   
        self.Bind(wx.EVT_CLOSE, self.onClose, id=wx.ID_CLOSE)  
        self.redrawTimer.Start(0.1)
        self.updateValueTimer.Start(0.1)

        self.graphBox = wx.BoxSizer(wx.VERTICAL)
        self.graphBox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW) 

        self.panel.SetSizer(self.graphBox)
        self.panel.Show()

        
    def onClose(self, event):
        """Event handler for closing."""
        self.redrawTimer.Stop()
        self.updateValueTimer.Stop()
        event.Skip()


    def updateValue(self, event):
        """Gets current value and updates it in the arrays. Also blinks PANDA led."""
        myPanda.setLedMode("ON")
        value = PandaDialogs.dataConversion(self.unit, self.Ks, self.Kf, self.Kt, self.Kp)
        now = time() - start

        avgSum = 0
        window = self.avgOver if self.avgOver < len(self.data) else len(self.data)
        for a in range(window):
            avgSum = avgSum + self.data[(-1 * a)]
        avgSum = avgSum / window
        self.avgData.append(float(avgSum))

        self.data.append(float(value))
        self.time.append(float(now))
        self.totalTime = now

        if len(self.data) > self.maximumArray:
            global looped
            if not looped:
                print ("Starting re-use of graph arrays for efficiency...")
                looped = True
            self.time.pop(0)
            self.avgData.pop(0)
            self.data.pop(0)

        self.fileTime.append(float(now))
        self.fileValue.append(float(value))
        self.fileAvg.append(float(avgSum))

        myPanda.setLedMode("OFF")

    def initPlot(self):
        """Initializes plot."""
        self.fig = Figure((self.width, (self.height)), dpi=self.dpi)

        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor('white')
        self.axes.set_title('Value and Average', size=12)
        self.axes.set_xlabel("Time (seconds)", size=10)
        if self.unit == 'strain':
            self.axes.set_ylabel("Strain", size=10)
        if self.unit == 'force/torques':
            self.axes.set_ylabel("Force (N) or Torque (N.m)", size=10)
        if self.unit == 'stress':
            self.axes.set_ylabel("Stress (N/m2)", size=10)

        plt.setp(self.axes.get_xticklabels(), fontsize=8)
        plt.setp(self.axes.get_yticklabels(), fontsize=8)

        self.plotData = self.axes.plot(
            self.data, 
            linewidth=2,
            color=(1, 0, 0),
            )[0]


        self.plotAvg = self.axes.plot(
            self.avgData, 
            linewidth=2,
            color=(0, 0, 1),
            )[0]

        self.Bind(wx.EVT_CLOSE, self.onClose)

    def drawPlot(self):
        """Draws plot when called."""
        gap = self.maximumData
        xmax = self.totalTime if self.totalTime > gap else gap      
        xmin = xmax - gap

        if self.unit == 'strain':
            ymin = -self.Ks*5
            ymax = self.Ks*5
        if self.unit == 'force/torque':
            ymin = -self.Kf*5
            ymax = self.Kf*5
        if self.unit == 'stress':
            ymin = -self.Kt*5
            ymax = self.Kt*5
        if self.unit == 'power':
            ymin = -self.Kp*5
            ymax = self.Kp*5
        #ymin = round(min(self.data), 3) - (1 * abs(round(min(self.data), 3)))
        #ymax = round(max(self.data), 3) + (1 * round(max(self.data), 3))
        #if (ymin == 0 and ymax == 0) or ymin == ymax:
            #ymax = self.Ks*10
            #ymin = -self.Ks*10

        self.axes.set_xbound(lower=xmin, upper=xmax)
        self.axes.set_ybound(lower=ymin, upper=ymax)
        
        self.axes.grid(True, color='gray')
        plt.setp(self.axes.get_xticklabels(), 
            visible=True)

        self.plotAvg.set_data(np.array(self.time), np.array(self.avgData))
        self.plotData.set_data(np.array(self.time), np.array(self.data))

        self.canvas.draw()

    def onRedrawTimer(self, event):      
        """Keeps calling drawPlot whenever the timer event is triggered."""
        self.drawPlot()

    def createMenu(self):
        """Creates menu where the user can choose to save an image or csv."""
        self.menuBar = wx.MenuBar()
        
        self.menuFile = wx.Menu()
        menuSaveCSV = self.menuFile.Append(-1, "&Salvar dados em .csv", "Save data to csv")
        self.Bind(wx.EVT_MENU, self.onSaveCSV, menuSaveCSV)
        menuSave = self.menuFile.Append(-1, "&Salvar imagem", "Save plot to image")
        self.Bind(wx.EVT_MENU, self.onSavePlot, menuSave)
        self.menuFile.AppendSeparator()
        menuExit = self.menuFile.Append(-1, "Parar aquisição\tCtrl-X", "Stop")
        self.Bind(wx.EVT_MENU, self.onClose, menuExit)
                
        self.menuBar.Append(self.menuFile, "&Arquivo")
        self.SetMenuBar(self.menuBar)

    def onSavePlot(self, event):
        """Saves the plot as an image."""
        fileChoices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=fileChoices,
            style=wx.FD_SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)

    def onSaveCSV(self, event):
        """Saves the data as a csv file."""
        fileChoices = "CSV (*.csv)|*.csv"
        
        dlg = wx.FileDialog(
            self, 
            message="Save data as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.csv",
            wildcard=fileChoices,
            style=wx.FD_SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            outFile = open(path, 'w')

            if self.unit == 'strain':
                outFile.write("Time,Strain,Avg\n")
            if self.unit == 'force/torque':
                outFile.write("Time,Force/Torque,Avg\n")
            if self.unit == 'stress':
                outFile.write("Time,Stress,Avg\n")
            if self.unit == 'power':
                outFile.write("Time,Power,Avg\n")

            for i in range(len(self.data)):
                outFile.write(str(self.fileTime[i]) + ",")
                outFile.write(str(self.fileValue[i]) + ",")
                outFile.write(str(self.fileAvg[i]) + "\n")
            outFile.close()