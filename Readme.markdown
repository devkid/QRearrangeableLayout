QRearrangeableLayout
====================

Using QSplitter elements to layout the widgets in your main window? This Qt Layout element, written in Python, lets the users rearrange the widgets, so that they can customize your application to there needs and preferences.

Download the python file [here](QRearrangeableLayout.py).

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

After this, you can either create a QSplitter object and set our ``rearrangeable`` as its parent:

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

You can now add widgets and other QSplitter elements to our ``splitter``. You may now set up some button or menu entry named »Rearrange« or similar which executes the following upon clicked:

```python
rearrangeable.setRearrangeable (True)
```
After clicking the button the user now can grab a widget inside your splitter hirarchy and drag it somewhere else.


Dragging
--------

Once the user grabbed a widget he can put it everythere he wants in your splitter hirarchy. He can do this by moving it to the top, to the left, to the right or to the bottom of another widget.

For example: you have two list widgets. The user wants to move the left one to the top of the second one. So he grabs the first list widget and moves the mouse to the top border of the second list widgets. The first widget then gets removed from the old horizontal splitter and a new vertical splitter is automatically created for these both list widgets.

However, for useability reasons, there are regions in the widgets the user can't drag the another widget to:
![widget](doc/widget.png)
If this was a widget, you couldn't drag another widget to the blue regions because otherwise you could not reach all of the green regions where you can drop your widget to. In our example, the user would drop the first list widget to the upper green region of the second list widget.

Now have a look at our example:
![screenshot 1](doc/screenshot1.png)

The user may now start dragging the left list widget:
![screenshot 2](doc/screenshot2.png)

... and when he reaches the green region (as mentioned above, not in the screenshot), the widgets get rearranged in a new vertical splitter:
![screenshot 3](doc/screenshot3.png)

You can find the source code for the test application [here](doc/test.py).