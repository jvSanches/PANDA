#----------------------------------------------------------------------

# Software da PANDA
# TCC - Engenharia Mecatrônica - Poli USP
# Guilherme de Agrela Lopes
# João Vitor Sanches
#
# SETTINGS FRAME
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

class SettingsFrame(wx.Frame):
    """
    This is the Settings Frame.  It shows all the options the user has:
    generate graphics, set amplifier gain, recalibrate the board or 
    choose Control modes.
    """
    def __init__(self, settings, parent, title):
        wx.Frame.__init__(self, parent, -1, title, 
                        pos=(450, 150), size=(600, 690))

        # Creates the Panel to put the other controls on
        self.panel = wx.Panel(self)

        # Initializes settings array
        self.settings = settings

        # Controls
        self.text = wx.StaticText(self.panel, -1, label="Selecione as configurações desejadas.", pos=(15, 5))
        self.text.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.text.SetSize(self.text.GetBestSize())

        self.btn_controlMode = wx.ToggleButton(self.panel, -1, label="Modo Controle", pos=(15, 35))
        self.btn_controlP = wx.RadioButton(self.panel, -1, label="Controle P", style=wx.RB_GROUP, pos=(130, 40))
        self.btn_controlPI = wx.RadioButton(self.panel, -1, label="Controle PI", pos=(130, 70))
        self.btn_controlPD = wx.RadioButton(self.panel, -1, label="Controle PD", pos=(130, 100))
        self.btn_controlPID = wx.RadioButton(self.panel, -1, label="Controle PID", pos=(130, 130))
        
        self.graphicsText = wx.StaticText(self.panel, -1, label="Mostrar Gráficos", pos=(15, 190))
        self.btn_showPolesZeros = wx.CheckBox(self.panel, -1, label="Gráfico de Polos e Zeros", pos=(130, 190))
        self.btn_showStepAnswer = wx.CheckBox(self.panel, -1, label="Resposta a Degrau", pos=(300, 190))
        self.btn_showRampAnswer = wx.CheckBox(self.panel, -1, label="Resposta a Rampa", pos=(440, 190))
        self.btn_showTorqueCurve = wx.CheckBox(self.panel, -1, label="Curva de Torque Característica", pos=(130, 220))
        self.btn_showValuesGraphic = wx.CheckBox(self.panel, -1, label="Gráficos dos Valores", pos=(330, 220))
        
        self.amplifierGainText = wx.StaticText(self.panel, -1, label="Ganho do Amplificador", pos=(15, 270))
        self.btn_amplifierGain = wx.SpinCtrl(self.panel, value='750', pos=(150, 270), min=0, max=1000)
        
        self.valuesText = wx.StaticText(self.panel, -1, label="Mostrar Valores", pos=(15, 320))
        self.btn_forces = wx.CheckBox(self.panel, -1, label="Forças", pos=(130, 320))
        self.btn_torques = wx.CheckBox(self.panel, -1, label="Torques", pos=(280, 320))
        self.btn_strains = wx.CheckBox(self.panel, -1, label="Deformações", pos=(130, 350))
        self.btn_powers = wx.CheckBox(self.panel, -1, label="Potências", pos=(280, 350))

        self.constantValuesText = wx.StaticText(self.panel, -1, label="Digite as constantes para cada valor:", pos=(15, 400))
        self.strainConstantText = wx.StaticText(self.panel, -1, label="Ks", pos=(130, 430))
        self.btn_strainConstant = wx.TextCtrl(self.panel, pos=(150, 430))
        self.forceConstantText = wx.StaticText(self.panel, -1, label="Kf", pos=(130, 460))
        self.btn_forceConstant = wx.TextCtrl(self.panel, pos=(150, 460))
        self.torqueConstantText = wx.StaticText(self.panel, -1, label="Kt", pos=(130, 490))
        self.btn_torqueConstant = wx.TextCtrl(self.panel, pos=(150, 490))
        self.powerConstantText = wx.StaticText(self.panel, -1, label="Kp", pos=(130, 520))
        self.btn_powerConstant = wx.TextCtrl(self.panel, pos=(150, 520))

        self.btn_saveSettings = wx.Button(self.panel, -1, label="Salvar Configurações", pos=(130, 600))
        self.btn = wx.Button(self.panel, -1, "Cancelar", pos=(330, 600))

        # Binds the controls to handlers
        self.Bind(wx.EVT_TOGGLEBUTTON, self.ToggleControl, self.btn_controlMode)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnSelectControlP, self.btn_controlP)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnSelectControlPI, self.btn_controlPI)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnSelectControlPD, self.btn_controlPD)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnSelectControlPID, self.btn_controlPID)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckControlBoxes, self.btn_showPolesZeros)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckControlBoxes, self.btn_showStepAnswer)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckControlBoxes, self.btn_showRampAnswer)

        self.Bind(wx.EVT_BUTTON, self.OnSaveSettingsButton, self.btn_saveSettings)
        self.Bind(wx.EVT_BUTTON, self.OnCancel, self.btn)

        # Prepare Frame based on settings array values
        if self.settings[0] == '0':
            self.btn_controlMode.SetValue(False)
            self.btn_controlP.Disable()
            self.btn_controlPI.Disable()
            self.btn_controlPD.Disable()
            self.btn_controlPID.Disable()

        elif self.settings[0] == 'P':
            self.btn_controlMode.SetValue(True)
            self.btn_controlP.SetValue(True)
            self.btn_controlPD.SetValue(False)
            self.btn_controlPI.SetValue(False)
            self.btn_controlPID.SetValue(False)
        elif self.settings[0] == 'PD':
            self.btn_controlMode.SetValue(True)
            self.btn_controlP.SetValue(False)
            self.btn_controlPD.SetValue(True)
            self.btn_controlPI.SetValue(False)
            self.btn_controlPID.SetValue(False)
        elif self.settings[0] == 'PI':
            self.btn_controlMode.SetValue(True)
            self.btn_controlP.SetValue(False)
            self.btn_controlPD.SetValue(False)
            self.btn_controlPI.SetValue(True)
            self.btn_controlPID.SetValue(False)
        elif self.settings[0] == 'PID':
            self.btn_controlMode.SetValue(True)
            self.btn_controlP.SetValue(False)
            self.btn_controlPD.SetValue(False)
            self.btn_controlPI.SetValue(False)
            self.btn_controlPID.SetValue(True)

        self.controlMode = self.settings[0]
        self.btn_showPolesZeros.SetValue(self.settings[1])
        self.btn_showStepAnswer.SetValue(self.settings[2])
        self.btn_showRampAnswer.SetValue(self.settings[3])
        self.btn_showTorqueCurve.SetValue(self.settings[4])
        self.btn_showValuesGraphic.SetValue(self.settings[5])

        self.btn_amplifierGain.SetValue(self.settings[6])

        self.btn_forces.SetValue(self.settings[7])
        self.btn_torques.SetValue(self.settings[8])
        self.btn_strains.SetValue(self.settings[9])
        self.btn_powers.SetValue(self.settings[10])

        self.btn_strainConstant.SetValue(str(self.settings[11]))
        self.btn_forceConstant.SetValue(str(self.settings[12]))
        self.btn_torqueConstant.SetValue(str(self.settings[13]))
        self.btn_powerConstant.SetValue(str(self.settings[14]))
 
        self.panel.Layout()


    def OnCancel(self, evt):
        """Event handler for closing."""
        self.Close()

    def ToggleControl(self, evt):
        """Event handler for the Control Toggle Button."""
        obj = evt.GetEventObject()
        isPressed = obj.GetValue()

        if isPressed:
            self.btn_controlP.Enable()
            self.btn_controlPI.Enable()
            self.btn_controlPD.Enable()
            self.btn_controlPID.Enable()
            if self.btn_controlP.GetValue():
                self.controlMode = 'P'
            if self.btn_controlPD.GetValue():
                self.controlMode = 'PD'
            if self.btn_controlPI.GetValue():
                self.controlMode = 'PI'
            if self.btn_controlPID.GetValue():
                self.controlMode = 'PID'

        else:
            self.btn_controlP.Disable()
            self.btn_controlPI.Disable()
            self.btn_controlPD.Disable()
            self.btn_controlPID.Disable()
            self.controlMode = '0'
            self.btn_showPolesZeros.SetValue(False)
            self.btn_showStepAnswer.SetValue(False)
            self.btn_showRampAnswer.SetValue(False)


    def OnSelectControlP(self, evt):
        """Event handler for the P control Radio Button."""
        self.controlMode = 'P'

    def OnSelectControlPD(self, evt):
        """Event handler for the PD control Radio Button."""
        self.controlMode = 'PD'

    def OnSelectControlPI(self, evt):
        """Event handler for the PI control Radio Button."""
        self.controlMode = 'PI'

    def OnSelectControlPID(self, evt):
        """Event handler for the PID control Radio Button."""
        self.controlMode = 'PID'

        
    def OnCheckControlBoxes(self, evt):
        """Event handler for the Checkboxes."""
        if not self.btn_controlMode.GetValue():
            controlNotActive_dialog = ControlNotActive(None, "Aviso")
            res = controlNotActive_dialog.ShowModal()
            if res == wx.ID_OK:
                controlNotActive_dialog.Destroy()

            self.btn_showPolesZeros.SetValue(False)
            self.btn_showStepAnswer.SetValue(False)
            self.btn_showRampAnswer.SetValue(False)


    def OnSaveSettingsButton(self, evt):
        """Event handler for the Save button."""
        self.settings[0] = self.controlMode
        self.settings[1] = self.btn_showPolesZeros.GetValue()
        self.settings[2] = self.btn_showStepAnswer.GetValue()
        self.settings[3] = self.btn_showRampAnswer.GetValue()
        self.settings[4] = self.btn_showTorqueCurve.GetValue()
        self.settings[5] = self.btn_showValuesGraphic.GetValue()
        self.settings[6] = self.btn_amplifierGain.GetValue()
        self.settings[7] = self.btn_forces.GetValue()
        self.settings[8] = self.btn_torques.GetValue()
        self.settings[9] = self.btn_strains.GetValue()
        self.settings[10] = self.btn_powers.GetValue()
        self.settings[11] = float(self.btn_strainConstant.GetValue())
        self.settings[12] = float(self.btn_forceConstant.GetValue())
        self.settings[13] = float(self.btn_torqueConstant.GetValue())
        self.settings[14] = float(self.btn_powerConstant.GetValue())

        self.Close()


    def GetSettings(self):
        """Returns settings array when asked."""
        return self.settings


class ControlNotActive(wx.Dialog):
    """
    This is a Dialog. It's opened when the user tries to select Control graphics
    when Control mode is not active.
    """
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, -1, title, 
                        pos=(650, 450), size=(500, 150))

        self.panel = wx.Panel(self)
        self.controlNotActiveText = wx.StaticText(self.panel, -1, label="Não é possível selecionar gráficos relacionados com Controle se ele não estiver ativo.", pos=(15,15))
        self.button_ok = wx.Button(self.panel, label="OK", pos=(210, 70))
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)

        self.panel.Layout()

    def onOk(self, e):
        """Event handler for the Ok button."""
        self.EndModal(wx.ID_OK)