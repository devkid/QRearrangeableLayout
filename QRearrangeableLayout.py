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

class QRearrangeableLayout (QWidget):
	
	"""Gets emitted, when the user started dragging a widget."""
	draggingStarted = pyqtSignal (QWidget, QPoint)
	
	"""Gets emitted, when the user ended dragging a widget by releasing the
	mouse button."""
	draggingEnded = pyqtSignal (QWidget, QPoint)
	
	
	def __init__ (self, app, parent = None):
		QWidget.__init__ (self, parent)
		
		self.app = app
		
		self.dragStarting = False
		self.dragRunning = False
		
		self.setAcceptDrops (True)
		
		self._rearrangeable = False
		
		self.app.installEventFilter (self)
	
	
	def setRearrangeable (self, rearrangeable):
		self._rearrangeable = bool (rearrangeable)
	
	
	def rearrangeable (self):
		return self._rearrangeable
	
	
	def removeWidget (self, widget):
		"""
		Removes a widget from its parent splitter. If the splitter is left with
		one or less widgets in it, it is removed from its parent itself and the
		(possibly) remaining widget is moved to the splitters parent.
		Returns the splitter if there are more then one widgets left in there,
		otherwise returns the parent of the splitter.
		"""
		
		splitter = widget.parent ()
		if not isinstance (splitter, QSplitter):
			raise TypeError ("Expecting a widget whose parent is a QSplitter")
		widget.setParent (None)
		parent = splitter.parent ()
		
		ret = splitter
		if splitter.count () < 2:
			# the splitter's parent is also a splitter, we only need to need to
			# move that one remaining widget to the parent
			if isinstance (parent, QSplitter):
				if splitter.count () == 1:
					child = splitter.widget (0)
					child.setParent (None)
					parent.insertWidget (parent.indexOf (splitter), child)
					ret = parent
			
			# if not: check if the remaining child is another splitter and if
			# so, change the splitters layout to the one of the remaining
			# splitter, move it's children to our top level splitter and
			# remove the remaining splitter afterwards
			else:
				if splitter.count () == 1:
					child = splitter.widget (0)
					if isinstance (child, QSplitter):
						ret = child
						splitter.setOrientation (child.orientation ())
						child.setParent (None)
						for i in reversed (range (child.count ())):
							w = child.widget (i)
							print w
							w.setParent (None)
							splitter.addWidget (w)
						return splitter
					# if we are the top level splitter and the remaining child
					# isn't a splitter, we must NOT put it standalone into the
					# splitters parent, because otherwise there wouldn't be any
					# top level splitter anymore
					#else:
					#	pass
			
			splitter.setParent (None)
			
		return ret
	
	
	@staticmethod
	def findChildOfSplitter (widget):
		"""
		Walk up the family tree of the given widget until it finds a widget
		whose parent is a QSplitter.
		Returns that widget.
		"""
		
		while widget <> None and not isinstance (widget.parent (), QSplitter):
			widget = widget.parent ()
		return widget
	
	
	def eventFilter (self, source, event):
		
		# ignore events that aren't going to our widget
		try:
			if not self.rect ().contains (event.pos ()):
				raise
		except:
			return QBoxLayout.eventFilter (self, source, event)
		
		if not self._rearrangeable:
			return QBoxLayout.eventFilter (self, source, event)
		
		if event.type () == QEvent.MouseButtonPress:
			self.dragSource = QRearrangeableLayout.findChildOfSplitter (source)
			
			if self.dragSource <> None:
				self.dragStarting = True
				self.dragPos = event.pos ()
			
			if isinstance (self.dragSource, QSplitterHandle):
				self.dragStarting = False
				
			if self.dragStarting:
				self.draggingStarted.emit (self.dragSource, event.pos ())
		
		elif event.type () == QEvent.MouseButtonRelease:
			self.dragStarting = False
		
		elif (event.type () == QEvent.MouseMove and
		     self.dragStarting and
		     (event.pos () - self.dragPos).manhattanLength () > QApplication.startDragDistance ()):
			self.dragStarting = False
			self.dragRunning = True
			
			# begin dragging procedure
			mimeData = QMimeData ()
			drag = QDrag (self.dragSource)
			drag.setMimeData (mimeData)
			drag.setHotSpot (self.dragPos)
			dropAction = drag.start (Qt.MoveAction)
			
		return QBoxLayout.eventFilter (self, source, event)
	
	
	def dragEnterEvent (self, e):
		
		# only accept dragging events (at least in our RearrangeableLayout) when
		# we started it manually (see above)
		e.setAccepted (self.dragRunning)
	
	
	def dragMoveEvent (self, e):
		
		# is the widget underneath parented by a QSplitter? if yes, put it there
		under = self.app.widgetAt (QCursor.pos ())
		widget = QRearrangeableLayout.findChildOfSplitter (under)
		if (widget in (None, self.dragSource) or
		   isinstance (widget, QSplitterHandle)):
			return
		splitter = widget.parent ()
		
		# the direction in which we want to expand:
		# 0 = up, 1 = right, 2 = left, 3 = down (order for arithmetic reasons)
		direction = 0
		i = 0
		
		pos = e.pos () - widget.mapTo (self, QPoint (0,0))
		size = widget.size ()
		w = size.width ()
		h = size.height ()
		d = (pos.x () * h) / w # function value of the diagonal
		
		cornersize = size / 4
		ww = w * 3/4
		wh = h * 3/4
		rects = [
			# disable a region in the middle of the widget,
			# half the size of the widget itself
			QRect (QPoint (cornersize.width (), cornersize.height ()), size / 2),
			
			# disable corner regions;
			# these regions touch the middle regions at one point
			QRect (QPoint (0,  0),  cornersize),
			QRect (QPoint (ww, 0),  cornersize),
			QRect (QPoint (0,  wh), cornersize),
			QRect (QPoint (ww, wh), cornersize)
		]
		for r in rects:
			# (need to ajust a bit, so that we don't collide with the borders,
			#  is a little bit strange)
			r.adjust (-10, -10, 10, 10)
			if r.contains (pos):
				return
		
		# calculate the direction in which to expand
		if pos.y () > d:
			direction += 2
		# ... ?
		if pos.y () > -d + h:
			direction += 1
		
		# break down to the actual direction and if we insert before or after
		# the widget underneath
		if direction in (0, 3):
			orientation = Qt.Vertical
		else:
			orientation = Qt.Horizontal
		before = direction % 2 == 0
		
		# do not remove ourselves just to push us back afterwards
		indexDrag = splitter.indexOf (self.dragSource)
		indexWidget = splitter.indexOf (widget)
		if (splitter.orientation () == orientation and
		   self.dragSource.parent () == splitter and
		   indexWidget + 1 - before - (self.dragSource.parent () == splitter and
		   indexDrag < indexWidget) == indexDrag):
			return
		
		splitter = self.removeWidget (self.dragSource)
		
		i = splitter.indexOf (widget)
		
		# this should "nearly" never happen, but it sometimes still does don't
		# know the reason right now, but it won't go bad if we insert the widget
		# at the first position
		if i < 0:
			i = 0
		
		if splitter.orientation () == orientation:
			
			# we want to insert the dragging source into the same direction the
			# underneath splitter already is so we just need to put it in there
			if not before:
				i += 1
			
			splitter.insertWidget (i, self.dragSource)
			
		else:
			# here we put the dragging widget and widget underneath the mouse
			# into a new splitter and put it to the index the widget was located
			# before
			
			widget.setParent (None)
			
			newSplitter = QSplitter (orientation)
			
			if before:
				newSplitter.addWidget (self.dragSource)
				newSplitter.addWidget (widget)
			else:
				newSplitter.addWidget (widget)
				newSplitter.addWidget (self.dragSource)
			
			splitter.insertWidget (i, newSplitter)
	
	
	def dropEvent (self, e):
		self.dragRunning = False
		self.draggingEnded.emit (self.dragSource, e.pos ())
