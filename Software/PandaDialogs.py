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

from panda_board import panda
import wx

myPanda = panda('auto')

def dataConversion(unit, Ks, Kf, Kt, Kp):
    '''
    V_i = 3.3
    V_o = myPanda.getAnalog1()/228249
    R = 350
    E = 70000000000
    GF = 2
    m = 0.1
    radius = 0.01
    I = m*radius*radius/2
    y = 0.001
    L = 0.1
    dV = V_o/V_i
    dR = (4*R*dV)/(V_i-2*dV)
    strain = dR/R*GF
    force = (E*strain*I)/(L*y)
    torque = (force*L)
    '''

    value = 3.3*((myPanda.getAnalog1()/2048) - 1)   # DAC value converted to Vout
    strain = Ks*value
    force = Kf*value
    torque = Kt*value
    power = Kp*value

    if unit == 'strain':
        return strain
    elif unit == 'force':
        return force
    elif unit == 'torque':
        return torque
    elif unit == 'power':
        return power
    else:
        print("Invalid unit!")



class PandaNotDetected(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, -1, title, 
                        pos=(650, 450), size=(500, 150))

        self.panel = wx.Panel(self)
        self.controlNotActiveText = wx.StaticText(self.panel, -1, label="Não foi detectado um PANDA. Por favor, cheque se o dispositivo está conectado e foi\n reconhecido, e então reinicie o programa.", pos=(15,15))
        self.button_ok = wx.Button(self.panel, label="OK", pos=(210, 70))
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)

        self.panel.Layout()

    def onOk(self, e):
        self.EndModal(wx.ID_OK)
