#----------------------------------------------------------------------

# Software da PANDA
# TCC - Engenharia Mecatrônica - Poli USP
# Guilherme de Agrela Lopes
# João Vitor Sanches
#
# MAIN FRAME
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
from wx.lib import plot as wxplot
from wx.lib.agw import hyperlink as wxhyperlink

from SettingsFrame import SettingsFrame
from CalibrationFrame import CalibrationFrame
from PlotFrame import PlotFrame
import PandaDialogs
from PandaDialogs import myPanda


class MainFrame(wx.Frame):
    """
    This is the Main Frame. It's the first screen the user will see, where
    they can decide what to do.
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title,
                          pos=(350, 350), size=(780, 280))

        # Creates the Panel to put the other controls on
        panel = wx.Panel(self)

        # Controls
        text = wx.StaticText(panel, -1, "Ois! Este é o software da placa PANDA. Por favor, selecione e salve as configurações desejadas. \nCaso seja sua primeira vez aqui, clique no Manual do Usuário.", pos=(15,15))
        text.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        lnk = wxhyperlink.HyperLinkCtrl(panel, -1, "Manual do Usuário", URL="https://github.com/jvSanches/PANDA/blob/master/README.md", pos=(325,150))
        btn_settings = wx.Button(panel, -1, "Configurações", pos=(75,90))
        btn_calibration = wx.Button(panel, -1, "Modo de Calibração", pos=(220,90))
        btn_graphics = wx.Button(panel, -1, "Mostrar Gráficos", pos=(395,90))
        btn_sendControlValues = wx.Button(panel, -1, "Valores do Controle", pos=(550,90))

        # Binds the controls to handlers
        self.Bind(wx.EVT_BUTTON, self.OnSettingsButton, btn_settings)
        self.Bind(wx.EVT_BUTTON, self.OnCalibrationButton, btn_calibration)
        self.Bind(wx.EVT_BUTTON, self.onGraphicsButton, btn_graphics)
        self.Bind(wx.EVT_BUTTON, self.OnSendControlButton, btn_sendControlValues)

        panel.Layout()
        
        # Initial value of arrays
        self.settings = ['0', False, False, False, False, False, '750', False, False, False, False, 0.0015, 4000, 45, 0, 0]
        self.calibration = [True, False, False, '0', '0', '0', 0]


    def OnTimeToClose(self, evt):
        """Event handler for closing."""
        myPanda.disconnect()
        self.Close()


    def OnSettingsButton(self, evt):
        """Event handler for the Settings button."""
        settings_frame = SettingsFrame(self.settings, parent=wx.GetTopLevelParent(self), title="Configurações")
        settings_frame.Show()


    def OnCalibrationButton(self, evt):
        """Event handler for the Calibration button."""
        cal = CalibrationFrame(self.calibration, parent=wx.GetTopLevelParent(self), title="Modo de Calibração")
        res = cal.Show()
            

    def onGraphicsButton(self, evt):
        """Event handler for the Graphics button."""
        if myPanda.exists():
            '''
            if self.settings[1] or self.settings[2] or self.settings[3] or self.settings[4] or self.settings[5]:
                if self.settings[15] == wx.ID_OK:
                    myPanda.setGain(self.settings[6])
                    self.settings[15] = 0

                
                if self.calibration[6] == wx.ID_OK:
                    if self.calibration[0]:
                        myPanda.runAutoOffset(int(2048*(((1/3.3)*(self.calibration[3]/self.settings[11])) + 1)))
                    if self.calibration[1]:
                        myPanda.runAutoOffset(int(2048*(((1/3.3)*(self.calibration[4]/self.settings[12])) + 1)))
                    if self.calibration[2]:
                        myPanda.runAutoOffset(2048*(((1/3.3)*(self.calibration[5]/self.settings[13])) + 1))
            '''

            if self.settings[5]:
                if self.settings[7]:
                    plot = PlotFrame('force', self.settings[11], self.settings[12], self.settings[13], self.settings[14], parent=wx.GetTopLevelParent(self), title="Gráfico da Força")
                    res = plot.Show()
                if self.settings[8]:
                    plot = PlotFrame('torque', self.settings[11], self.settings[12], self.settings[13], self.settings[14], parent=wx.GetTopLevelParent(self), title="Gráfico do Torque")
                    res = plot.Show()
                if self.settings[9]:
                    plot = PlotFrame('strain', self.settings[11], self.settings[12], self.settings[13], self.settings[14], parent=wx.GetTopLevelParent(self), title="Gráfico da Deformação")
                    res = plot.Show()
                if self.settings[10]:
                    plot = PlotFrame('power', self.settings[11], self.settings[12], self.settings[13], self.settings[14], parent=wx.GetTopLevelParent(self), title="Gráfico da Potência")
                    res = plot.Show()
            if (not self.settings[1]) and (not self.settings[2]) and (not self.settings[3]) and (not self.settings[4]) and (not self.settings[5]):
                noGraphicSelected_dialog = NoGraphicSelected(None, "Aviso")
                res = noGraphicSelected_dialog.ShowModal()
                if res == wx.ID_OK:
                    noGraphicSelected_dialog.Destroy()
        else:
            pandaNotDetected_dialog = PandaDialogs.PandaNotDetected(None, "Aviso")
            res = pandaNotDetected_dialog.ShowModal()
            if res == wx.ID_OK:
                pandaNotDetected_dialog.Destroy()
            

    def OnSendControlButton(self, evt):
        """Event handler for the Control button."""
        notImplemented_dialog = NotYetImplemented(None, "Aviso")
        res = notImplemented_dialog.ShowModal()
        if res == wx.ID_OK:
            notImplemented_dialog.Destroy()


class NoGraphicSelected(wx.Dialog):
    """
    This is a Dialog. It's opened when the user tries to open graphics
    but haven't checked any box in Settings.
    """
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, -1, title, 
                        pos=(650, 450), size=(500, 150))

        self.panel = wx.Panel(self)
        self.controlNotActiveText = wx.StaticText(self.panel, -1, label="Não foi selecionado nenhum gráfico. Por favor, selecione algum nas Configurações.", pos=(15,15))
        self.button_ok = wx.Button(self.panel, label="OK", pos=(210, 70))
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)

        self.panel.Layout()

    def onOk(self, e):
        """Event handler for the Ok button."""
        self.EndModal(wx.ID_OK)


class NotYetImplemented(wx.Dialog):
    """
    This is a Dialog. It's opened when the user tries to open a frame
    that hasn't yet been implemented.
    """
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, -1, title, 
                        pos=(650, 450), size=(500, 150))

        self.panel = wx.Panel(self)
        self.controlNotActiveText = wx.StaticText(self.panel, -1, label="Ainda será implementado!", pos=(15,15))
        self.button_ok = wx.Button(self.panel, label="OK", pos=(210, 70))
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)

        self.panel.Layout()

    def onOk(self, e):
        """Event handler for the Ok button."""
        self.EndModal(wx.ID_OK)

'''
class MyPopupMenu(wx.Menu):

    def __init__(self, parent):
        super(MyPopupMenu, self).__init__()

        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Minimize')
        self.Append(mmi)
        self.Bind(wx.EVT_MENU, self.OnMinimize, mmi)

        cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        self.Append(cmi)
        self.Bind(wx.EVT_MENU, self.OnClose, cmi)

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()
'''


class MyApp(wx.App):
    """
    Class to start the program.
    """
    def OnInit(self):
        frame = MainFrame(None, "PANDA Software")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True
        

# Runs the program
app = MyApp(redirect=True)
app.MainLoop()
wx.Exit()