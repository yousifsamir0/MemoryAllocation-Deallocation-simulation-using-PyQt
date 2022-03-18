import sys
from Model.classes import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPointF, QRectF, Qt, QCoreApplication, QProcess
from PyQt5.QtGui import QColor, QFont, QIcon, QPainter, QBrush, QPen
from Model import style_copy


class process_GUI(QGroupBox):
    def __init__(self, process=None):
        QGroupBox.__init__(self)
        self.process = Process() if process == None else process
        #self.lblname = QLabel(f"{self.process.name}")
        self.setTitle(f"{self.process.name}")
        self.dealloc = QPushButton("Kill")
        self.dealloc.setMaximumWidth(50)
        self.setMaximumHeight(100)
        self.setMaximumWidth(250)
        self.organize()

    def organize(self):
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.dealloc, 0, 0)

    def add_segment(self, name, size, start_add=-1):
        self.process.add_seg(name, size, start_add)


class startScreen(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowIcon(QIcon("icon.png"))
        self.holesnum = 2
        self.sizee = 0
        add_holeB = QPushButton("Add Hole...")
        add_holeB.clicked.connect(self.add_hole)
        done_butt = QPushButton("Done")
        done_butt.clicked.connect(self.donee)

        rowlayout = QHBoxLayout()
        rowlayout.addWidget(QLabel("start address:"))
        rowlayout.addWidget(QLineEdit())
        rowlayout.addWidget(QLabel("size:"))
        rowlayout.addWidget(QLineEdit())

        self.form = QFormLayout()
        self.form.addRow("1:   ", rowlayout)

        butt_container = QHBoxLayout()
        butt_container.addWidget(add_holeB)
        butt_container.addWidget(done_butt)

        groupbox = QGroupBox()
        groupbox.setTitle("Add Holes:")
        groupbox.setLayout(self.form)

        leftscroll = QScrollArea()
        leftscroll.setWidget(groupbox)
        leftscroll.setWidgetResizable(True)
        leftscroll.setViewportMargins(10, 10, 10, 10)
        leftscroll.setMaximumWidth(350)
        leftscroll.setMinimumHeight(195)

        self.method = "ff"
        self.method_butt = QPushButton("FirstFit")
        self.method_butt.setCheckable(True)
        self.method_butt.clicked.connect(self.toggle)

        self.sizeform = QFormLayout()
        self.sizeform.addRow("Memory Size (Defauly:256) :", QLineEdit())
        self.sizeform.addRow("Allocation Method: ", self.method_butt)

        vlayout = QVBoxLayout(self)
        vlayout.addWidget(leftscroll)
        vlayout.addLayout(self.sizeform)
        vlayout.addLayout(butt_container)

    def toggle(self):
        if self.method_butt.isChecked():
            self.method = "bf"
            self.method_butt.setText("BestFit")

        else:
            self.method = "ff"
            self.method_butt.setText("FirstFit")

    def add_hole(self):
        rowlayout = QHBoxLayout()
        rowlayout.addWidget(QLabel("start address:"))
        rowlayout.addWidget(QLineEdit())
        rowlayout.addWidget(QLabel("size:"))
        rowlayout.addWidget(QLineEdit())
        self.form.addRow(f"{self.holesnum}:   ", rowlayout)
        self.holesnum += 1

    def donee(self):
        memsize = self.sizeform.itemAt(1).widget().text()
        memsize = int((memsize)) if memsize != "" else 256
        self.sizee = memsize
        sizecheck = 0
        if (memsize > 0):
            self.memory = Memory(memsize)

        n = int(self.form.count() / 2.0)
        for i in range(n):
            start_add = self.form.itemAt(2 * i +
                                         1).layout().itemAt(1).widget().text()
            size = self.form.itemAt(2 * i +
                                    1).layout().itemAt(3).widget().text()
            if not ((start_add == "") | (size == "")):
                sizecheck += int(size)
                if (sizecheck <= self.sizee):
                    self.memory.add_hole(int(start_add), int(size))
        self.done(1)


class Dialoge(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowIcon(QIcon("add.png"))
        self.segnum = 2
        self.segments = []
        add_segment = QPushButton("Add segment..")
        add_segment.clicked.connect(self.add_seg)
        done_butt = QPushButton("Done")
        done_butt.clicked.connect(self.donee)

        rowlayout = QHBoxLayout()
        rowlayout.addWidget(QLabel("name"))
        rowlayout.addWidget(QLineEdit())
        rowlayout.addWidget(QLabel("size"))
        rowlayout.addWidget(QLineEdit())

        self.form = QFormLayout()
        self.form.addRow("1:   ", rowlayout)

        butt_container = QHBoxLayout()
        butt_container.addWidget(add_segment)
        butt_container.addWidget(done_butt)

        groupbox = QGroupBox()
        groupbox.setTitle("Add Segments")
        groupbox.setLayout(self.form)

        leftscroll = QScrollArea()
        leftscroll.setWidget(groupbox)
        leftscroll.setWidgetResizable(True)
        leftscroll.setViewportMargins(10, 10, 10, 10)
        leftscroll.setMaximumWidth(350)
        leftscroll.setMinimumHeight(350)

        vlayout = QVBoxLayout(self)
        vlayout.addWidget(leftscroll)
        vlayout.addLayout(butt_container)

    def add_seg(self):
        rowlayout = QHBoxLayout()
        rowlayout.addWidget(QLabel("name"))
        rowlayout.addWidget(QLineEdit())
        rowlayout.addWidget(QLabel("size"))
        rowlayout.addWidget(QLineEdit())
        # for i in range(rowlayout.count()):
        #     print(rowlayout.itemAt(i))

        self.form.addRow(f"{self.segnum}:   ", rowlayout)
        self.segnum += 1

    def donee(self):
        formlen = int(self.form.count() / 2)
        for i in range(formlen):
            name = self.form.itemAt(2 * i +
                                    1).layout().itemAt(1).widget().text()
            size = self.form.itemAt(2 * i +
                                    1).layout().itemAt(3).widget().text()
            if not ((name == "") | (size == "")):
                self.segments.append([name, int(size)])
        self.done(0)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.GUIprocesses = []
        self.initUI()
        self.setObjectName("main")

    def initUI(self):
        # ------------------------------------start_screen-------------------------------
        start = startScreen()
        start.setWindowTitle("Memory Allocation - Memory initialize")
        start.setFixedWidth(350)
        start.setMaximumHeight(500)
        start.setMinimumHeight(150)

        if (start.exec() == 0):
            sys.exit()
        self.memory = start.memory
        self.method = start.method
        if not len(self.memory.holes):
            self.memory = Memory(start.sizee)
            self.memory.add_hole(0, start.sizee)
        self.memory.detect_old_p()

        # ------------------------------------LEFT Layout--------------------------------

        proc_groupbox = QGroupBox()
        leftscroll = QScrollArea()
        leftscroll.setWidget(proc_groupbox)
        leftscroll.setWidgetResizable(True)
        leftscroll.setFixedHeight(550)
        leftscroll.setMaximumWidth(200)
        leftscroll.setObjectName("P")

        self.layoutproc = QFormLayout()
        # self.layoutproc.addStretch(100)
        #self.layoutproc.setContentsMargins(1, 1, 1, 1)

        proc_groupbox.setLayout(self.layoutproc)
        proc_groupbox.setTitle("Processes list")

        layouttopleft = QHBoxLayout()
        layoutleft = QVBoxLayout()

        self.add_p = QPushButton("Add Process")
        self.add_p.setMaximumWidth(200)
        self.add_p.clicked.connect(self.alloc)

        self.reset_button = QPushButton("New Memory")
        self.reset_button.clicked.connect(self.restart)

        # self.deall = QPushButton("De-allocate")
        # self.deall.setMaximumWidth(70)
        # self.deall.clicked.connect(self.updatee)

        butt_container = QWidget()
        butt_container.setLayout(layouttopleft)
        butt_container.setFixedWidth(300)

        layouttopleft.addWidget(self.add_p)
        layouttopleft.addWidget(self.reset_button)
        # layouttopleft.addWidget(self.deall)
        layouttopleft.addStretch(0)
        layouttopleft.setSpacing(10)
        layouttopleft.setContentsMargins(0, 0, 0, 5)

        layoutleft.addWidget(butt_container)
        layoutleft.addWidget(leftscroll)
        layoutleft.addStretch(1)
        layoutleft.setSpacing(1)

        # --------------------------------------Right layout---------------------------
        self.layoutright = QVBoxLayout()

        # ---------------------------------------
        outerlayout = QHBoxLayout(self)
        outerlayout.addLayout(layoutleft)
        outerlayout.addLayout(self.layoutright)
        outerlayout.addStretch(0)

        for process in self.memory.oldP:
            self.oldP_GUI(process)

    def alloc(self):
        dial = Dialoge()
        dial.setWindowTitle("Add process")
        dial.setModal(True)
        dial.exec()
        segnum = len(dial.segments)
        if (segnum > 0):
            newprocessGUI = process_GUI()

            for seg in dial.segments:
                newprocessGUI.add_segment(seg[0], seg[1])
            self.memory.Add_process(newprocessGUI.process, self.method)
            # if (is_fit==None):
            #    self.GUIprocesses.append(newprocessGUI)
            #    self.layoutproc.addRow(newprocessGUI)

            if newprocessGUI.process.is_alloc:
                newprocessGUI.setObjectName("yes")
                self.GUIprocesses.append(newprocessGUI)
                self.layoutproc.addRow(newprocessGUI)

            else:
                newprocessGUI.setObjectName("no")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText("Process Dosen't fit !!!")
                msg.setWindowTitle("Error")
                msg.exec_()
            newprocessGUI.dealloc.clicked.connect(
                lambda: self.dealloc(newprocessGUI))
            self.update()

    def oldP_GUI(self, process):
        newprocessGUI = process_GUI(process)
        self.GUIprocesses.append(newprocessGUI)
        self.layoutproc.addRow(newprocessGUI)
        newprocessGUI.dealloc.clicked.connect(
            lambda: self.dealloc(newprocessGUI))

    def dealloc(self, GUIprocess):
        Pname = GUIprocess.process.name
        self.memory.de_alloc(GUIprocess.process)
        self.GUIprocesses.remove(GUIprocess)
        listsize = self.layoutproc.count()
        for i in range(listsize):
            item = self.layoutproc.itemAt(i).widget()
            if item != None:
                if item.process.name == Pname:
                    item.deleteLater()
                    break
        self.update()
        # for proc in self.memory.oldP:
        # print(proc.name)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        painter.setFont(QFont("Sans-serif", 12))
        hpx = 500
        width = 200
        height = (hpx / self.memory.size)
        y = (hpx / self.memory.size)
        x = 350.0
        Voffset = 90
        i = 1
        painter.drawText(
            QPointF(x + width + 5, (self.memory.size * y + Voffset)),
            f"{self.memory.size-1}")
        # --------------------------------holes paint-----------------
        for hole in self.memory.holes:
            painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
            sa = hole.start_add
            siz = hole.size
            rect = QRectF(x, (sa * y) + Voffset, width, siz * height)
            painter.drawRect(rect)
            painter.drawText(rect, Qt.AlignCenter, f"Hole {i}")
            painter.drawText(QPointF(x + width + 5, (sa * y) + Voffset),
                             f"{sa}")
            i += 1
        # --------------------------------processes paint-------------------
        for process in self.memory.processes:
            painter.setBrush(QBrush(QColor("#82b6ff"), Qt.SolidPattern))
            for seg in process.segments:
                sa = seg.start_add
                siz = seg.size
                rect = QRectF(x, int(sa * y) + Voffset, width, siz * height)
                painter.drawRect(rect)
                painter.drawText(rect, Qt.AlignCenter,
                                 f"{process.name}:{seg.name}")
                painter.drawText(QPointF(x + width + 5, (sa * y) + Voffset),
                                 f"{sa}")
        # --------------------------------OLDprocesses paint---------------------------
        for process in self.memory.oldP:
            painter.setBrush(QBrush(QColor("#4b45ff"), Qt.SolidPattern))
            for seg in process.segments:
                sa = seg.start_add
                siz = seg.size
                rect = QRectF(x, int(sa * y) + Voffset, width, siz * height)
                painter.drawRect(rect)
                painter.drawText(rect, Qt.AlignCenter,
                                 f"{process.name}:{seg.name}")
                painter.drawText(QPointF(x + width + 5, (sa * y) + Voffset),
                                 f"{sa}")

    def restart(self):
        qm = QMessageBox
        quest = qm.question(self, 'New Memory',
                            "All Processes will get deleted, Continue ?",
                            qm.Yes | qm.No)

        if quest == qm.Yes:
            QCoreApplication.quit()
            status = QProcess.startDetached(sys.executable, sys.argv)
        else:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_copy.DarkBreeze())
    ex = App()
    # ex.setStyleSheet(DarkBreeze())
    ex.setGeometry(200, 50, 900, 600)
    ex.setWindowTitle("Memory Allocation")
    ex.setWindowIcon(QIcon("icon.png"))
    ex.setFixedWidth(600)
    ex.setFixedHeight(600)
    ex.show()
    sys.exit(app.exec_())
