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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import xml.dom.minidom as dom

from QRearrangeableLayout import QRearrangeableLayout

class QRearrangeableLayoutLoader:
	
	def __init__ (self, rearrangeable):
		self.rearrangeable = rearrangeable
		self.widgets = {}

		if self.rearrangeable.layout () == None:
			self.rearrangeable.setLayout (QHBoxLayout ())

	def registerWidget (self, name, widget):
		# mark the widget for later saving
		widget.__QRearrangeableLayoutLoader_name = name
		self.widgets [name] = widget

	def unregisterWidget (self, nameOrWidget):
		if isinstance (nameOrWidget, str):
			QRearrangeableLayout.removeWidget (self.widgets [nameOrWidget])
			del self.widgets [nameOrWidget]
			return
		elif isinstance (nameOrWidget, QWidget):
			name = [n for n, w in self.widgets.iteritems () if v == nameOrWidget][0]
			self.unregisterWidget (name)
			return
		raise KeyError ("No such widget: " + repr (nameOrWidget))


	### ------------------------------------------------------------------------
	### Code for loading

	def load (self, f):
		"""
		Fills the managed QRearrangeableLayout with QSplitters and the given
		widgets with the given widths bases on the XML file given.
		"""

		tree = dom.parse (f)

		self._load (self.rearrangeable.layout (), tree.firstChild, True)

	@staticmethod
	def _createSplitter (node):
		o = node.getAttribute ("o")
		if o == "h":
			o = Qt.Horizontal
		elif o == "v":
			o = Qt.Vertical
		else:
			raise TypeError ("Unknown orientation for splitter: " + o)
		return QSplitter (o)

	def _load (self, p, t, first = False):
		found = False
		s = 0
		sizes = []
		ssum = 0
		for n in t.childNodes:
			valid = True
			if n.nodeName == "s":
				if first and found:
					raise IndexError ("There are more then one top level elements!")
				splitter = QRearrangeableLayoutLoader._createSplitter (n)
				p.addWidget (splitter)
				self._load (splitter, n)
				found = True
			elif n.nodeName == "w":
				if first:
					raise TypeError ("Unexpected widget at top level!")
				name = n.getAttribute ("n")
				if not name in self.widgets:
					raise IndexError ("Unknown widget: " + name)
				p.addWidget (self.widgets [name])
			else:
				valid = False
			if valid and not first and s <> -1:
				print n
				wstr = n.getAttribute ("s")
				try:
					if wstr == "":
						s = -1
					else:
						s = float (wstr)
						ssum += s
						sizes.append (s)
				except (ValueError):
					raise ValueError ("Undefined size: " + wstr)

		# set sizes of child widgets
		if not first and s <> -1:
			for i in range (len (sizes)):
				if p.orientation == Qt.Horizontal:
					s = p.size ().width ()
				else:
					s = p.size ().height ()
				sizes [i] *= s / ssum
			print sizes
			p.setSizes (sizes)


	### ------------------------------------------------------------------------
	### Code for saving
	
	def save (self, f):
		"""
		Saves the structure of the managed QRearrangeableLayout into the XML
		file given.
		"""

		if self.rearrangeable.layout ().count () < 0:
			return

		root = dom.Element ("rearrangeable")
		self._save (self.rearrangeable.layout (), root, True)

		root.writexml (open (f, "w"), "", "\t", "\n")

	@staticmethod
	def _getSplitterOrientationAsString (splitter):
		if splitter.orientation () == Qt.Horizontal:
			return "h"
		else:
			return "v"
		
	def _save (self, p, t, first = False):
		if not first:
			sizes = p.sizes ()
			if p.orientation () == Qt.Horizontal:
				size = p.size ().width ()
			else:
				size = p.size ().height ()
		
		for i in range (p.count ()):
			if first:
				w = p.itemAt (i).widget ()
			else:
				w = p.widget (i)
			if isinstance (w, QSplitter):
				# avoid redundancy
				if not first and w.orientation () == p.orientation ():
					self._save (w, t)
					continue
				else:
					elem = dom.Element ("s")
					elem.setAttribute ("o", QRearrangeableLayoutLoader._getSplitterOrientationAsString (w))
					self._save (w, elem)
			elif isinstance (w, QWidget):
				elem = dom.Element ("w")
				elem.setAttribute ("n", w.__QRearrangeableLayoutLoader_name)

			if not first:
				# one one-thousandth precision is enough
				elem.setAttribute ("s", "%.3f" % (float (sizes [i]) / float (size)))

			t.appendChild (elem)
