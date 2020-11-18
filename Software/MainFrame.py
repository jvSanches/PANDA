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
#
# Tutoriais em http://zetcode.com/wxpython/menustoolbars/
# Também tem tutoriais em C:\Users\User\Anaconda3\Lib\site-packages\wx\lib
# Live Data Graphing: https://www.phidgets.com/docs21/Live_Data_Graphing
# Live Data Reading from USB: https://stackoverflow.com/questions/19908167/reading-serial-data-in-realtime-in-python
# Creating Excel file: https://xlsxwriter.readthedocs.io/index.html?highlight=creating%20excel%20files%20with%20python
# Making an Executable: https://datatofish.com/executable-pyinstaller/
# How to distribute a wxPython application: https://www.blog.pythonlibrary.org/2019/03/19/distributing-a-wxpython-application/
    # pyinstaller --onefile GUI.py --noconsole

#----------------------------------------------------------------------
 
import wx
from wx.lib import plot as wxplot
from wx.lib.agw import hyperlink as wxhyperlink
import xlsxwriter

from SettingsFrame import SettingsFrame
from CalibrationFrame import CalibrationFrame
from PlotFrame import PlotFrame
from HistoryFrame import HistoryFrame
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

        # Create the menubar
        #menuBar = wx.MenuBar()

        # Create the menu
        #menu = wx.Menu()

        # add an item to the menu, using \tKeyName automatically
        # creates an accelerator, the third param is some help text
        # that will show up in the statusbar
        '''
        menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Exit this simple sample")

        menu.Append(wx.ID_NEW, '&New\tCtrl-N')
        menu.Append(wx.ID_OPEN, '&Open\tCtrl-O')
        menu.Append(wx.ID_SAVE, '&Save\tCtrl-S')
        menu.AppendSeparator()

        imp = wx.Menu()
        imp.Append(wx.ID_ANY, 'Import newsfeed list...')
        imp.Append(wx.ID_ANY, 'Import bookmarks...')
        imp.Append(wx.ID_ANY, 'Import mail...')

        menu.Append(wx.ID_ANY, 'I&mport', imp)

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnTimeToClose, id=wx.ID_EXIT)

        # and put the menu on the menubar
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()
        '''

        # Now create the Panel to put the other controls on.
        panel = wx.Panel(self)

        # and a few controls
        text = wx.StaticText(panel, -1, "Ois! Este é o software da placa PANDA. Por favor, selecione e salve as configurações desejadas. \nCaso seja sua primeira vez aqui, clique no Manual do Usuário.", pos=(15,15))
        text.SetFont(wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD))
        text.SetSize(text.GetBestSize())
        lnk = wxhyperlink.HyperLinkCtrl(panel, -1, "Manual do Usuário", URL="https://github.com/jvSanches/PANDA/blob/master/README.md", pos=(325,150))
        #btn_readme = wx.Button(panel, -1, title=lnk, pos=(145,90))
        btn_settings = wx.Button(panel, -1, "Configurações", pos=(75,90))
        btn_calibration = wx.Button(panel, -1, "Modo de Calibração", pos=(220,90))
        btn_graphics = wx.Button(panel, -1, "Mostrar Gráficos", pos=(395,90))
        #btn_history = wx.Button(panel, -1, "Mostrar Histórico")
        btn_sendControlValues = wx.Button(panel, -1, "Valores do Controle", pos=(550,90))
        #btn_exportSpreadsheet = wx.Button(panel, -1, "Exportar planilha com os valores")

        # bind the button events to handlers
        #self.Bind(wx.EVT_BUTTON, self.OnReadmeButton, btn_readme)
        self.Bind(wx.EVT_BUTTON, self.OnSettingsButton, btn_settings)
        self.Bind(wx.EVT_BUTTON, self.OnCalibrationButton, btn_calibration)
        self.Bind(wx.EVT_BUTTON, self.onGraphicsButton, btn_graphics)
        #self.Bind(wx.EVT_BUTTON, self.onHistoryButton, btn_history)
        self.Bind(wx.EVT_BUTTON, self.OnSendControlButton, btn_sendControlValues)
        #self.Bind(wx.EVT_BUTTON, self.OnExportSpreadsheetButton, btn_exportSpreadsheet)

        # Use a sizer to layout the controls, stacked vertically and with
        # a 10 pixel border around each
        '''
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text, 0, wx.ALL, 10)
        sizer.Add(btn_readme, 0, wx.ALL, 10)
        sizer.Add(btn_settings, 0, wx.ALL, 10)
        sizer.Add(btn_calibration, 0, wx.ALL, 10)
        sizer.Add(btn_graphics, 0, wx.ALL, 10)
        #sizer.Add(btn_history, 0, wx.ALL, 10)
        sizer.Add(btn_sendControlValues, 0, wx.ALL, 10)
        #sizer.Add(btn_exportSpreadsheet, 0, wx.ALL, 10)
        panel.SetSizer(sizer)
        '''
        panel.Layout()


        # Maximum total time (seconds) to be displayed on x axis 
        self.maximumData = 60
        # Number of data points before cropping the visual graph arrays
        self.maximumArray = 3000 
        

        self.settings = ['0', False, False, False, False, False, '750', False, False, False, False, 0.0015, 400, 4500, 0]
        self.calibration = [True, False, False, '0', '0', '0']


    def OnTimeToClose(self, evt):
        """Event handler for the button click."""
        #print ("Até logo!")
        self.Close()

    '''
    def OnReadmeButton(self, evt):
        """Event handler for the button click."""
        #print ("Envia para a página do Readme")
        wxhyperlink.HyperLinkCtrl.GotoURL(self, "https://github.com/jvSanches/PANDA/blob/master/README.md", ReportErrors=False, NotSameWinIfPossible=False)
        visited = wxhyperlink.HyperLinkCtrl.SetVisited(self,Visited=False)
    '''

    def OnSettingsButton(self, evt):
        """Event handler for the button click."""
        #print ("Abre o popup com as opções de configuração")
        settings_frame = SettingsFrame(self.settings, parent=wx.GetTopLevelParent(self), title="Configurações")
        res = settings_frame.Show()
        if res == wx.ID_OK:
            self.settings = settings_frame.GetSettings()
            myPanda.setGain(self.settings[6])


    def OnCalibrationButton(self, evt):
        """Event handler for the button click."""
        #print ("Entra no modo de calibração")
        cal = CalibrationFrame(self.calibration, parent=wx.GetTopLevelParent(self), title="Modo de Calibração")
        res = cal.Show()
        if res == wx.ID_OK:
            self.calibration = cal.GetCal()
            if self.calibration[0]:
                myPanda.runAutoOffset(2048*(((1/3.3)*(self.calibration[3]/self.settings[11])) + 1))
            if self.calibration[1]:
                myPanda.runAutoOffset(2048*(((1/3.3)*(self.calibration[4]/self.settings[12])) + 1))
            if self.calibration[2]:
                myPanda.runAutoOffset(2048*(((1/3.3)*(self.calibration[5]/self.settings[13])) + 1))

        

    def onGraphicsButton(self, evt):
        """Event handler for the button click."""
        #print ("Mostra o histórico de valores lidos")

        if myPanda.exists():
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

    '''
    def onHistoryButton(self, evt):

        if myPanda.exists():
            if self.settings[7]:
                history = HistoryFrame('force', parent=wx.GetTopLevelParent(self), title="Histórico - Força")
                history.Show()
            if self.settings[8]:
                history = HistoryFrame('torque', parent=wx.GetTopLevelParent(self), title="Histórico - Torque")
                history.Show()
            if self.settings[9]:
                history = HistoryFrame('strain', parent=wx.GetTopLevelParent(self), title="Histórico - Deformação")
                history.Show()

        else:
            pandaNotDetected_dialog = PandaDialogs.PandaNotDetected(parent=wx.GetTopLevelParent(self), title="Aviso")
            res = pandaNotDetected_dialog.ShowModal()
            if res == wx.ID_OK:
                pandaNotDetected_dialog.Destroy()
    '''
            

    def OnSendControlButton(self, evt):
        """Event handler for the button click."""
        #print ("Envia as variáveis de Controle")

        notImplemented_dialog = NotYetImplemented(None, "Aviso")
        res = notImplemented_dialog.ShowModal()
        if res == wx.ID_OK:
            notImplemented_dialog.Destroy()

    '''
    def OnExportSpreadsheetButton(self, evt):
        """Event handler for the button click."""
        print ("Exporta uma planilha do Excel com os dados")

        # Create a workbook and add a worksheet
        workbook = xlsxwriter.Workbook('Acquired_Values.xlsx')
        worksheet = workbook.add_worksheet()

        # Add a bold format to use to highlight cells
        bold = workbook.add_format({'bold': 1})

        # Add a number format for cells with money.
        money_format = workbook.add_format({'num_format': '$#,##0'})

        # Add an Excel date format.
        date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

        # Adjust the column width.
        worksheet.set_column(1, 1, 15)

        # Write some data headers.
        worksheet.write('A1', 'Tempo', bold)
        worksheet.write('B1', 'Deformação', bold)
        worksheet.write('C1', 'Força', bold)
        worksheet.write('D1', 'Torque', bold)

        # Some data we want to write to the worksheet.
        values = (
        [1, 54, 1000, 547],
        [2,  789,  100, 5478],
        [3, 24.7,  300, 540],
        [4,  41.0,   50, 0],
        )

        # Start from the first cell below the headers.
        row = 1
        col = 0

        # Write values
        for time, deformation, force, torque in (values):
            worksheet.write_number(row, col, time)
            worksheet.write_number(row, col+1, deformation)
            worksheet.write_number(row, col+2, force)
            worksheet.write_number(row, col+3, torque)
            row += 1

        # Write a total using a formula.
        row = 5
        worksheet.write(row, 0, 'Total', bold)
        worksheet.write(row, 1, '=SUM(B2:B5)')
        worksheet.write(row, 2, '=SUM(C2:C5)')
        worksheet.write(row, 3, '=SUM(D2:D5)')

        workbook.close()
    '''


class NoGraphicSelected(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, -1, title, 
                        pos=(650, 450), size=(500, 150))

        self.panel = wx.Panel(self)
        self.controlNotActiveText = wx.StaticText(self.panel, -1, label="Não foi selecionado nenhum gráfico. Por favor, selecione algum nas Configurações.", pos=(15,15))
        self.button_ok = wx.Button(self.panel, label="OK", pos=(210, 70))
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)

        self.panel.Layout()

    def onOk(self, e):
        self.EndModal(wx.ID_OK)


class NotYetImplemented(wx.Dialog):
    def __init__(self, parent, title):
        wx.Dialog.__init__(self, parent, -1, title, 
                        pos=(650, 450), size=(500, 150))

        self.panel = wx.Panel(self)
        self.controlNotActiveText = wx.StaticText(self.panel, -1, label="Ainda será implementado!", pos=(15,15))
        self.button_ok = wx.Button(self.panel, label="OK", pos=(210, 70))
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)

        self.panel.Layout()

    def onOk(self, e):
        self.EndModal(wx.ID_OK)


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



        


class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, "PANDA Software")
        self.SetTopWindow(frame)

        #print ("Print statements go to this stdout window by default.")

        frame.Show(True)
        return True
        

app = MyApp(redirect=True)
app.MainLoop()
wx.Exit()