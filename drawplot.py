# This Python file uses the following encoding: utf-8
import sys
import datetime
import time
import random
from PySide2.QtWidgets import QApplication, QMainWindow
import pyqtgraph as pg
from PySide2.QtCore import QTimer

x = []
y = []
n = 0


class drawPlot(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        self.setWindowTitle("Cross hair floating Lable ")
        self.axis = pg.DateAxisItem(orientation='bottom')
        self.pDraw = pg.GraphicsLayoutWidget(show=True)
        self.pDraw.setBackground((0, 0, 0))
        self.setCentralWidget(self.pDraw)
        #Create plot and add Items to it
        self.p1 = self.pDraw.addPlot(row=0, col=0, axisItems={'bottom': pg.DateAxisItem(orientation='bottom')})
        self.curve1 = self.p1.plot()
        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.label = pg.TextItem("")
        self.p1.addItem(self.label, ignoreBounds=False)
        self.p1.addItem(self.vLine, ignoreBounds=True)
        self.p1.addItem(self.hLine, ignoreBounds=True)

        #initialize Timer, connect its timout Event Signal to UpdatePlot Slot
        self.timer_update_events = QTimer()
        self.timer_update_events.timeout.connect(self.updatePlot)
        self.timer_update_events.start(200)

        #initialize Crosshair lable  and connect mouse movment to mouseMoved
        self.vb = self.p1.vb
        self.proxy = pg.SignalProxy(self.p1.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        self.updatePlot()
        self.label.setPos(x[0],0)



    def mouseMoved(self, evt):

                pos = evt[0]
                if self.p1.sceneBoundingRect().contains(pos):
                    mousePoint = self.vb.mapSceneToView(pos)
                    intMousePoint = int(mousePoint.x())
                    if intMousePoint > 0:
                         self.vLine.setPos(mousePoint.x())
                         self.hLine.setPos(mousePoint.y())
                         self.label.setPos(mousePoint)
                         self.label.setHtml("<br><span style='font-size: 8pt'>x= %s \
                                             <br><span style='color: red'>y1= %0.1f</span>" \
                                             % (datetime.datetime.utcfromtimestamp(intMousePoint).strftime('%H:%M:%S'), mousePoint.y()))

    #
    def updatePlot(self):
                    global x, y, n
                    #generate random number and populate x with it
                    n = n + random.uniform(-1, 1)
                    x.append(time.time())
                    y.append(random.uniform(0, 1) + n)

                    pen = pg.mkPen(clear=True, color=(255, 160, 240), width=1)
                    self.curve1.setData(x, y, pen=pen)






if __name__ == "__main__":
    app = QApplication([])
    window = drawPlot()
    window.show()
    sys.exit(app.exec_())
