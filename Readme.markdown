QRearrangeableLayout
====================

Using QSplitter elements to layout the widgets in your main window? This Qt
Layout element, written in Python, lets the users rearrange the widgets, so that
they can customize your application to their needs and preferences.

Usage
-----

First import the module:

```python
from QRearrangeableLayout import QRearrangeableLayout
```

Now you can instantiate a QRearrangeableLayout object:

```python
rearrangeable = QRearrangeableLayout (app)
```
make sure to give a reference to the appliction as parameter.

After this, you can either create a QSplitter object and set our
``rearrangeable`` as its parent:

```python
splitter = QSplitter (Qt.Horizontal, rearrangeable)
```
or you can use a layout to arrange your splitter:

```python
boxlayout = QHBoxLayout ()
rearrangeable.setLayout (boxlayout)
splitter = QSplitter (Qt.Horizontal)
boxlayout.addWidget (rearrangeable)
```

Note: Please use one of these two methods! It might cause problems if you try
and nest multiple QBoxLayouts and add QSplitter elements as widgets to these
nested layouts. Also, be warned that, if you add a QLayout to a nested splitter
and then add another QSplitter to this layout, the user will be able to
rearrange the widgets in this QSplitter, but not interchange it with the other
widgets of the top level splitter. If you don't want the user to be able to
rearrange some of your widgets, set an attribute like this:

```python
widget.__QRearrangeable_notRearrangeable = True
```

Note that this will only apply to actual widgets and not to QSplitter elements
nor to their children widgets.

You can now add widgets and other QSplitter elements to our ``splitter``. You
may now set up some button or menu entry named »Rearrange« or similar which
executes the following upon clicked:

```python
rearrangeable.setRearrangeable (True)
```
After clicking the button the user now can grab a widget inside your splitter
hirarchy and drag it somewhere else.


Dragging
--------

Once the user grabbed a widget he can put it everythere he wants in your
splitter hirarchy. He can do this by moving it to the top, to the left, to the
right or to the bottom of another widget.

For example: you have two list widgets. The user wants to move the left one to
the top of the second one. So he grabs the first list widget and moves the mouse
to the top border of the second list widgets. The first widget then gets removed
from the old horizontal splitter and a new vertical splitter is automatically
created for these both list widgets.

However, for useability reasons, there are regions in the widgets the user can't
drag the another widget to:

![widget](https://raw.github.com/devkid/QRearrangeableLayout/master/doc/widget.png)

If this was a widget, you couldn't drag another widget to the blue regions
because otherwise you could not reach all of the green regions where you can
drop your widget to. In our example, the user would drop the first list widget
to the upper green region of the second list widget.

Now have a look at our example:

![screenshot 1](https://raw.github.com/devkid/QRearrangeableLayout/master/doc/screenshot1.png)

The user may now start dragging the left list widget:

![screenshot 2](https://raw.github.com/devkid/QRearrangeableLayout/master/doc/screenshot2.png)

... and when he reaches the green region (as mentioned above, not in the
screenshot), the widgets get rearranged in a new vertical splitter:

![screenshot 3](https://raw.github.com/devkid/QRearrangeableLayout/master/doc/screenshot3.png)

You can find the source code for the test application in `doc/example.py`.


QRearrangeableLayoutLoader
--------------------------

Here is a self explaining example of how to load save the layouts the user made:

```python
from QRearrangeableLayoutLoader import QRearrangeableLayoutLoader

# create window, lists, rearrangeable and so on

# ...

loader = QRearrangeableLayoutLoader (rearrangeable)
loader.registerWidget ("list1", list1)
loader.registerWidget ("list2", list2)
loader.load ("example2.xml")
```

As you can see, you can register your available widgets to this loader class
and it will automatically generate QSplitter elements and put your widgets in
there as specified in the given XML file.

You can save the layout in quite the same way:
```python
loader.save ("example2.xml")
```

Here is an example of how our initial layout of the first example would look
like in XML:

```xml
<rearrangeable>
	<s o="h">
		<w n="list1" w="0.5"/>
		<w n="list2" w="0.5"/>
	</s>
</rearrangeable>
```

Note: At the top level there must be exactly one »s« (splitter) entity. The »w«
attribute (relative width) might only applied to non-top level entities (both
splitter and widget). (TODO - will be implemented later)
