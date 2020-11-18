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

import wx

class CalibrationFrame(wx.Frame):
    """
    This is MyFrame.  It just shows a few controls on a wxPanel,
    and has a simple menu.
    """
    def __init__(self, calibration, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(350, 250), size=(600, 350))

         # Now create the Panel to put the other controls on.
        self.panel = wx.Panel(self)

        self.calibration = calibration

        # and a few controls
        self.text = wx.StaticText(self.panel, -1, label="Digite o valor de deformação, força ou torque aplicado.", pos=(15, 15))
        self.text.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.text.SetSize(self.text.GetBestSize())

        self.btn_optStrain = wx.RadioButton(self.panel, -1, label="Deformação", style=wx.RB_GROUP, pos=(15, 95))
        self.btn_optForce = wx.RadioButton(self.panel, -1, label="Força", pos=(210, 95))
        self.btn_optTorque = wx.RadioButton(self.panel, -1, label="Torque", pos=(375, 95))
        
        self.btn_strainValue = wx.SpinCtrl(self.panel, value='0', pos=(110, 90), min=0, max=1000)
        self.btn_forceValue = wx.SpinCtrl(self.panel, value='0', pos=(270, 90), min=0, max=1000)
        self.btn_torqueValue = wx.SpinCtrl(self.panel, value='0', pos=(440, 90), min=0, max=1000)
        
        self.btn_confirmChoices = wx.Button(self.panel, -1, label="Aplicar", pos=(140, 200))
        self.btn = wx.Button(self.panel, -1, "Cancelar", pos=(340, 200))

        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.OnTimeToClose, self.btn)
        self.Bind(wx.EVT_RADIOBUTTON, self.SelectStrain, self.btn_optStrain)
        self.Bind(wx.EVT_RADIOBUTTON, self.SelectForce, self.btn_optForce)
        self.Bind(wx.EVT_RADIOBUTTON, self.SelectTorque, self.btn_optTorque)
        self.Bind(wx.EVT_BUTTON, self.OnConfirmButton, self.btn_confirmChoices)


        if self.calibration[0]:
            self.btn_strainValue.Enable()
        else:
            self.btn_strainValue.Disable()
        if self.calibration[1]:
            self.btn_forceValue.Enable()
        else:
            self.btn_forceValue.Disable()
        if self.calibration[2]:
            self.btn_torqueValue.Enable()
        else:
            self.btn_torqueValue.Disable()
        self.btn_optStrain.SetValue(self.calibration[0])
        self.btn_optForce.SetValue(self.calibration[1])
        self.btn_optTorque.SetValue(self.calibration[2])
        self.btn_strainValue.SetValue(self.calibration[3])
        self.btn_forceValue.SetValue(self.calibration[4])
        self.btn_torqueValue.SetValue(self.calibration[5])

        self.panel.Layout()


    def SelectStrain(self, evt):
        """Event handler for the button click."""
        print ("Ativa/Desativa o modo de Controle")

        self.btn_strainValue.Enable()
        self.btn_forceValue.Disable()
        self.btn_torqueValue.Disable()


    def SelectForce(self, evt):
        """Event handler for the button click."""
        print ("Ativa/Desativa o modo de Controle")

        self.btn_strainValue.Disable()
        self.btn_forceValue.Enable()
        self.btn_torqueValue.Disable()


    def SelectTorque(self, evt):
        """Event handler for the button click."""
        print ("Ativa/Desativa o modo de Controle")

        self.btn_strainValue.Disable()
        self.btn_forceValue.Disable()
        self.btn_torqueValue.Enable()


    def OnConfirmButton(self, evt):
        """Event handler for the button click."""
        print ("Salva as configurações escolhidas do popup")

        self.calibration[0] = self.btn_optStrain.GetValue()
        self.calibration[1] = self.btn_optForce.GetValue()
        self.calibration[2] = self.btn_optTorque.GetValue()
        self.calibration[3] = self.btn_strainValue.GetValue()
        self.calibration[4] = self.btn_forceValue.GetValue()
        self.calibration[5] = self.btn_torqueValue.GetValue()

        self.Close()


    def OnTimeToClose(self, evt):
        """Event handler for the button click."""
        print ("Até logo!")
        self.Close()
        

    def GetCal(self):
        return self.calibration