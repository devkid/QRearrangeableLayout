#
# Copyright (C) by Alfred Krohmer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# Visit http://qrearrangeablelayout.github.com/ for further information
#

from QRearrangeableLayout import QRearrangeableLayout

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys, signal

class Window (QMainWindow):

	def __init__ (self, app):
		QMainWindow.__init__ (self)
		self.resize (800, 600)
		
		self.app = app
		
		self.setWindowTitle ("QRearrangeableLayout - Test")
		
		self.list1 = QListWidget ()
		self.list1.addItem (QListWidgetItem ("List1"))
		self.list2 = QListWidget ()
		self.list2.addItem (QListWidgetItem ("List2"))
		for i in range (0,10):
			self.list1.addItem (QListWidgetItem ("Another item"))
			self.list2.addItem (QListWidgetItem ("Another item"))
		
		self.central = QRearrangeableLayout (self.app, self)
		self.central.setRearrangeable (True)
		self.setCentralWidget (self.central)
		
		self.mainhbox = QHBoxLayout ()
		self.central.setLayout (self.mainhbox)
		
		self.hbox = QSplitter (Qt.Horizontal)
		self.hbox.addWidget (self.list1)
		self.hbox.addWidget (self.list2)
		
		self.mainhbox.addWidget (self.hbox)

app = QApplication (sys.argv)
signal.signal (signal.SIGINT, signal.SIG_DFL)

window = Window (app)
window.show ()

app.exec_ () 
