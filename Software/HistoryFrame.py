#----------------------------------------------------------------------

# Software da PANDA
# TCC - Engenharia Mecatrônica - Poli USP
# Guilherme de Agrela Lopes
# João Vitor Sanches
#
#
# Arquivos:
# MainFrame: Tela principal; chamada das outras classes
# CalibrationFrame: Tela para realizar a calibração da placa; criada ao clicar no botão 'Modo de Calibração' da tela principal
# HistoryFrame: Tela para selecionar o histórico das leituras da placa e geração de arquivo .csv do período selecionado; criada ao clicar no botão 'Mostrar Histórico'
# PlotFrame: Telas com os gráficos gerados a partir das seleções na tela de Configuração; criadas ao clicar no botão 'Mostrar Gráficos'
# SettingsFrame: Tela para escolher as configurações desejadas do programa; criada ao clicar no botão 'Configurações'
# PandaDialogs: Diálogos de erro relacionados com a PANDA
# panda_board: Interação do software com o firmware da PANDA

#----------------------------------------------------------------------

import locale
import wx
from time import time
import os
import PandaDialogs
from PandaDialogs import myPanda

# Globals
looped = False
start = time()


class HistoryFrame(wx.Frame):
    def __init__(self, chooseUnit, parent, title):

        self.dpi = 100
        self.height = 5
        self.width = 10

        wx.Frame.__init__(self, parent, -1, title,
                            pos=((self.width * self.dpi)-500, (self.height * self.dpi)), size=(1200,800))

        self.unit = chooseUnit

        self.maximumData = 60
        self.maximumArray = 3000

        initialValue = PandaDialogs.dataConversion(self.unit)

        self.avgOver = 50

        self.data = [initialValue]
        self.time = [0]
        self.avgData = [initialValue]

        self.totalTime = 0

        self.fileTime = [0]
        self.fileValue = [initialValue]

        self.panel = wx.Panel(self, -1)

        self.createMenu()

        self.updateValueTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateValue, self.updateValueTimer)      
        self.updateValueTimer.Start(100)

        self.panel.Show()

        
    def onClose(self, event):
        self.updateValueTimer.Stop()
        self.Destroy()


    def updateValue(self, event):

        myPanda.setLedMode("ON")
        value = PandaDialogs.dataConversion(self.unit)
        now = time()

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

        myPanda.setLedMode("OFF")


    def createMenu(self):
        self.menuBar = wx.MenuBar()
        
        self.menuFile = wx.Menu()
        menuSaveCSV = self.menuFile.Append(-1, "&Save plot as CSV", "Save data to csv")
        self.Bind(wx.EVT_MENU, self.onSaveCSV, menuSaveCSV)
        menuSave = self.menuFile.Append(-1, "&Save plot as image", "Save plot to image")
        self.Bind(wx.EVT_MENU, self.onSavePlot, menuSave)
        self.menuFile.AppendSeparator()
        menuExit = self.menuFile.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.onClose, menuExit)
                
        self.menuBar.Append(self.menuFile, "&File")
        self.SetMenuBar(self.menuBar)


    def onSaveCSV(self, event):
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
            outFile.write("Time,Strain\n")
        if self.unit == 'force':
            outFile.write("Time,Force\n")
        if self.unit == 'torque':
            outFile.write("Time,Torque\n")

            for i in range(len(self.data)):
                outFile.write(str(self.fileTime[i]) + ",")
                outFile.write(str(self.fileValue[i]) + "\n")
            outFile.close()