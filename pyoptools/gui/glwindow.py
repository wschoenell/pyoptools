#!/usr/bin/env python

# This includes the two classes wxGLWindow and wxAdvancedGLWindow
# from OpenGL.TK in the PyOpenGL distribution
# ported to wxPython by greg Landrum
# modified by Y. Wong
# modified by R. Amezquita
# modified by O. Olarte

from OpenGL.GL import *
from OpenGL.GLU import *
from wx import *
from wx.glcanvas import *
import math
import os,sys

def test_data(npoints):
    #A simple testing function that generate random triangles
    # 10 random points (x,y) in the plane
    import numpy
    import matplotlib.delaunay as triang
    x,y =  numpy.array(numpy.random.standard_normal((2,npoints)))
    z =  numpy.array(numpy.random.standard_normal(npoints))
    points=[]
    for i in range(npoints):
            points.append((x[i],y[i],z[i]))
    cens,edg,tri,neig = triang.delaunay(x,y)
    return points, tri 
    
def glTranslateScene(s, x, y, mousex, mousey):
    glMatrixMode(GL_MODELVIEW)
    mat = glGetDoublev(GL_MODELVIEW_MATRIX)
    glLoadIdentity()
    glTranslatef(s * (x - mousex), s * (mousey - y), 0.0)
    glMultMatrixd(mat)



def glRotateScene(s, xcenter, ycenter, zcenter, x, y, mousex, mousey):
    glMatrixMode(GL_MODELVIEW)
    mat = glGetDoublev(GL_MODELVIEW_MATRIX)
    glLoadIdentity()
    glTranslatef(xcenter, ycenter, zcenter)
    glRotatef(s * (y - mousey), 1., 0., 0.)
    glRotatef(s * (x - mousex), 0., 1., 0.)
    glTranslatef(-xcenter, -ycenter, -zcenter)
    glMultMatrixd(mat)

def v3distsq(a,b):
  d = ( a[0] - b[0], a[1] - b[1], a[2] - b[2] )
  return d[0]*d[0] + d[1]*d[1] + d[2]*d[2]

# This code is needed to avoid faults on sys.exit()
import sys
oldexitfunc = None
if hasattr(sys, 'exitfunc'):
    oldexitfunc = sys.exitfunc
def cleanup():
    if oldexitfunc: oldexitfunc()
sys.exitfunc = cleanup

class wxGLWindow(GLCanvas):
  """Implements a simple wxPython OpenGL window.

  This class provides a simple window, into which GL commands can be issued. This is done by overriding the built in functions InitGL(), DrawGL(), and FinishGL(). The main difference between it and the plain wxGLCanvas is that it copes with refreshing and resizing the window"""
  def __init__(self, parent,*args,**kw):
    self.GL_uninitialised = 1
    apply(GLCanvas.__init__,(self, parent)+args, kw)
    EVT_SIZE(self,self.wxSize)
    EVT_PAINT(self,self.wxPaint)
    EVT_ERASE_BACKGROUND(self, self.wxEraseBackground)
    self.w, self.h = self.GetClientSizeTuple()

  def __del__(self):
    #      self.SetCurrent()
    self.FinishGL()

  def InitGL(self):
    """OpenGL initialisation routine (to be overridden).
    This routine, containing purely OpenGL commands, should be overridden by the user to set up the GL scene.
	If it is not overridden, it defaults to setting an ambient light, setting the background colour to gray, 
	and enabling GL_DEPTH_TEST and GL_COLOR_MATERIAL."""
    #set up lighting
    glLightfv(GL_LIGHT0, GL_AMBIENT, [1.0, 1.0, 1.0, 1.0])
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glClearColor(0.7,0.7,0.7,0.0)
    glShadeModel(GL_SMOOTH)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
   
  def FinishGL(self):
    """OpenGL closing routine (to be overridden).

    This routine should be overridden if necessary by any OpenGL commands need to be specified when deleting the GLWindow (e.g. deleting Display Lists)."""
    pass

  def DrawGL(self):
    """OpenGL drawing routine (to be overridden).
    This routine, containing purely OpenGL commands, should be overridden by the user to draw the GL scene. 
	If it is not overridden, it defaults to drawing a colour cube."""
    #Draw colour cube
    glBegin(GL_QUAD_STRIP)
    glColor3f(1.0,1.0,1.0) #corner 1
    glNormal3f(0.57735027, 0.57735027, 0.57735027)
    glVertex3f(0.5, 0.5, 0.5)
    glColor3f(1.0,0.0,1.0) #corner 2
    glNormal3f(0.57735027, -0.57735027, 0.57735027)
    glVertex3f(0.5, -0.5, 0.5)
    glColor3f(1.0,1.0,0.0) #corner 3
    glNormal3f(0.57735027, 0.57735027, -0.57735027)
    glVertex3f(0.5, 0.5, -0.5)
    glColor3f(1.0,0.0,0.0) #corner 4
    glNormal3f(0.57735027, -0.57735027, -0.57735027)
    glVertex3f(0.5, -0.5, -0.5)
    glColor3f(0.0,1.0,0.0) #corner 5
    glNormal3f(-0.57735027, 0.57735027, -0.57735027)
    glVertex3f(-0.5, 0.5, -0.5)
    glColor3f(0.0,0.0,0.0) #corner 6
    glNormal3f(-0.57735027, -0.57735027, -0.57735027)
    glVertex3f(-0.5, -0.5, -0.5)
    glColor3f(0.0,1.0,1.0) #corner 7
    glNormal3f(-0.57735027, 0.57735027, 0.57735027)
    glVertex3f(-0.5, 0.5, 0.5)
    glColor3f(0.0,0.0,1.0) #corner 8
    glNormal3f(-0.57735027, -0.57735027, 0.57735027)
    glVertex3f(-0.5, -0.5, 0.5)
    glColor3f(1.0,1.0,1.0) #corner 1
    glNormal3f(0.57735027, 0.57735027, 0.57735027)
    glVertex3f(0.5, 0.5, 0.5)
    glColor3f(1.0,0.0,1.0) #corner 2
    glNormal3f(0.57735027, -0.57735027, 0.57735027)
    glVertex3f(0.5, -0.5, 0.5)
    glEnd()

    glBegin(GL_QUADS)
    glColor3f(1.0,1.0,1.0) #corner 1
    glNormal3f(0.57735027, 0.57735027, 0.57735027)
    glVertex3f(0.5, 0.5, 0.5)
    glColor3f(1.0,1.0,0.0) #corner 3
    glNormal3f(0.57735027, 0.57735027, -0.57735027)
    glVertex3f(0.5, 0.5, -0.5)
    glColor3f(0.0,1.0,0.0) #corner 5
    glNormal3f(-0.57735027, 0.57735027, -0.57735027)
    glVertex3f(-0.5, 0.5, -0.5)
    glColor3f(0.0,1.0,1.0) #corner 7
    glNormal3f(-0.57735027, 0.57735027, 0.57735027)
    glVertex3f(-0.5, 0.5, 0.5)
    glColor3f(1.0,0.0,1.0) #corner 2
    glNormal3f(0.57735027, -0.57735027, 0.57735027)
    glVertex3f(0.5, -0.5, 0.5)
    glColor3f(1.0,0.0,0.0) #corner 4
    glNormal3f(0.57735027, -0.57735027, -0.57735027)
    glVertex3f(0.5, -0.5, -0.5)
    glColor3f(0.0,0.0,0.0) #corner 6
    glNormal3f(-0.57735027, -0.57735027, -0.57735027)
    glVertex3f(-0.5, -0.5, -0.5)
    glColor3f(0.0,0.0,1.0) #corner 8
    glNormal3f(-0.57735027, -0.57735027, 0.57735027)
    glVertex3f(-0.5, -0.5, 0.5)
    glEnd()

  def wxSize(self, event = None):
    """Called when the window is resized"""
    self.w,self.h = self.GetClientSizeTuple()
    if self.GetContext():
      self.SetCurrent()
      glViewport(0, 0, self.w, self.h)
    self.Update()

  def wxEraseBackground(self, event):
    """Routine does nothing, but prevents flashing"""
    pass

  def wxPaint(self, event=None):
    """Called on a paint event.

    This sets the painting drawing context, then calls the base routine wxRedrawGL()"""
    dc = PaintDC(self)
    self.wxRedrawGL(event)
    
  def wxRedraw(self, event=None):
    """Called on a redraw request

    This sets the drawing context, then calls the base routine wxRedrawGL(). It can be called by the user when a refresh is needed"""
    dc = ClientDC(self)
    self.wxRedrawGL(event)

  def wxRedrawGL(self, event=None):
    """This is the routine called when drawing actually takes place.

    It needs to be separate so that it can be called by both paint events and by other events. It should not be called directly"""

    self.SetCurrent()

    if self.GL_uninitialised:
      glViewport(0, 0, self.w, self.h)
      self.InitGL()
      self.GL_uninitialised=0
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW);

    glPushMatrix();
    self.DrawGL()           # Actually draw here
    glPopMatrix();
    glFlush()               # Flush
    self.SwapBuffers()  # Swap buffers

    if event: event.Skip()  # Pass event up
    
    self.Update()

class wxAdvancedGLWindow(wxGLWindow):
  """Implements a wxPython OpenGL window allowing spinning, zooming, etc.

  This class is derived from wxGLWindow, and can be used in exactly the
  same way, by overriding the functions InitGL(), FinishGL(), and DrawGL()
  with functions containing OpenGL commands. The window captures mouse
  events, and keypresses. You might want to override some of these
  functions if you need more sophisticated control"""
  def __init__(self, parent,*args,**kw):
    if kw.has_key('autospin_allowed'):
      # Is the widget allowed to autospin?
      self.autospin_allowed = kw['autospin_allowed']
      del kw['autospin_allowed']
    else:
      self.autospin_allowed = 0
    apply(wxGLWindow.__init__,(self, parent)+args, kw)

    # The _back color
    self.r_back = 0.
    self.g_back = 0.
    self.b_back = 0.

    # Where the eye is
    #self.base_distance = self.distance = 10.0

    self.base_distance = self.distance = 1000.0

    # Field of view in y direction
    self.fovy = 30.0

    # Position of clipping planes.
    self.near = 0.1
    self.far = 10000.0

    # Where we are centering.
    self.xcenter = 0.0
    self.ycenter = 0.0
    self.zcenter = 0.0

    self.parent = parent
    # Current coordinates of the mouse.
    self.xmouse = 0
    self.ymouse = 0

    self.xspin = 0
    self.yspin = 0

    # Is the widget currently autospinning?
    self.autospin = 0

    self.initLeft = (0,0)

    EVT_SIZE(self,self.wxSize)
    EVT_PAINT(self,self.wxPaint)
    EVT_ERASE_BACKGROUND(self, self.wxEraseBackground)
    EVT_CHAR(self,self.OnChar)
    EVT_LEFT_DOWN(self,self.OnLeftClick)
    EVT_LEFT_DCLICK(self,self.OnLeftDClick)
    EVT_LEFT_UP(self,self.OnLeftUp)
    EVT_MIDDLE_DOWN(self,self.OnMiddleClick)
    EVT_RIGHT_DOWN(self,self.OnRightClick)
    EVT_RIGHT_DCLICK(self,self.OnRightDClick)
    EVT_MOTION(self,self.wxMouseMotion)
    EVT_IDLE(self,self.wxIdle)

  def wxIdle(self,event):
    if self.autospin:
#      self.do_AutoSpin(event) #doing it this way hogs the cpu
#      event.RequestMore()     #doing it this way hogs the cpu

      WakeUpIdle()
      self.do_AutoSpin(event)
      event.Skip(1)

  def OnChar(self,event):
    key = event.GetKeyCode()
    if key == ord('a'):
      self.autospin_allowed = not self.autospin_allowed
    if self.autospin:
      self.autospin = 0
    elif key == ord('q'):
      self.parent.Destroy()

  def OnLeftClick(self,event):
    self.wxRecordMouse(event)
    self.initLeft = event.GetX(),event.GetY()
  def OnLeftDClick(self,event):
    self.wxRecordMouse(event)
    self.reset()
  def OnLeftUp(self,event):
    if not event.m_shiftDown:
      self.wxAutoSpin(event)
  def OnMiddleClick(self,event):
    self.wxRecordMouse(event)
  def OnRightClick(self,event):
    self.wxRecordMouse(event)
  def OnRightDClick(self,event):
    self.wxRecordMouse(event)
    self.distance=self.base_distance
    self.wxRedraw()
  def OnLeftDrag(self,event):
    self.wxRotate(event)
  def OnMiddleDrag(self,event):
    self.wxTranslate(event)
  def OnRightDrag(self,event):
    self.wxScale(event)
  def wxMouseMotion(self,event):
    if not event.Dragging():
      return
    if event.LeftIsDown():
      self.OnLeftDrag(event)
    elif event.MiddleIsDown():
      self.OnMiddleDrag(event)
    elif event.RightIsDown():
      self.OnRightDrag(event)

  def report_opengl_errors(message = "OpenGL error:"):
    """Report any opengl errors that occured while drawing."""

    while 1:
      err_value = glGetError()
      if not err_value: break
      print message, gluErrorString(err_value)

  def SetBgColour(self, r, g, b):
    """Change the background colour of the widget.

    There seems to be a problem with this:"""

    self.r_back = r
    self.g_back = g
    self.b_back = b

    self.wxRedraw()

  def SetCenterpoint(self, x, y, z):
    """Set the new center point for the model.

    This is where we are looking."""

    self.xcenter = x
    self.ycenter = y
    self.zcenter = z

    self.wxRedraw()

  def set_base_distance(self, distance):
    """Set how far the eye is from the position we are looking.

    Sets the base distance, to which we are returned if we double click"""
    self.base_distance = distance

  def set_distance(self, distance):
    """Set how far the eye is from the position we are looking."""
    self.distance = distance
    self.wxRedraw()

  def reset(self):
    """Reset rotation matrix for this widget."""

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity()
    self.wxRedraw()

#  def wxHandlePick(self, event):
#    """Handle a pick on the scene."""
#    pass

  def wxRecordMouse(self, event):
    """Record the current mouse position."""
    self.xmouse = event.GetX()
    self.ymouse = event.GetY()

  def wxStartRotate(self, event):
    # Switch off any autospinning if it was happening
    self.autospin = 0
    self.wxRecordMouse(event)

  def wxScale(self, event):
    """Scale the scene.  Achieved by moving the eye position."""
    scale = 1 - 0.01 * (event.GetY() - self.ymouse)
    self.distance = self.distance * scale
    self.wxRedraw()
    self.wxRecordMouse(event)

  def do_AutoSpin(self,event):
    s = 0.5

    glRotateScene(0.5,
                  self.xcenter, self.ycenter, self.zcenter,
                  self.yspin, self.xspin, 0, 0)
    self.wxRedraw()

  def wxAutoSpin(self, event):
    """Perform autospin of scene."""

    if self.autospin_allowed:
      self.autospin = 1
      self.yspin = .1 * (event.GetX()-self.initLeft[0])
      self.xspin = .1 * (event.GetY()-self.initLeft[1])
      if self.xspin == 0 and self.yspin == 0:
        self.autospin = 0
      else:
        self.do_AutoSpin(event)


  def wxRotate(self, event):
    """Perform rotation of scene."""
    if not event.m_shiftDown:
      glRotateScene(0.5,
                    self.xcenter, self.ycenter, self.zcenter,
                    event.GetX(), event.GetY(), self.xmouse, self.ymouse)
    else:
      # rotate about z
      sz = self.GetClientSizeTuple()
      sz = (sz[0]/2, sz[1]/2)
      xp = event.GetX()
      yp = event.GetY()
      dy = (self.ymouse-yp)
      dx = (self.xmouse-xp)
      if yp > sz[1]:
        dx = dx * -1
      if xp < sz[0]:
        dy = dy * -1
      d = dx + dy
      glMatrixMode(GL_MODELVIEW);
      m = glGetDouble(GL_MODELVIEW_MATRIX)
      glLoadIdentity()
      glTranslatef(self.xcenter,self.ycenter,self.zcenter)
      glRotatef(.5*d,0,0,1.)
      glTranslatef(-self.xcenter,-self.ycenter,-self.zcenter)
      #glMultMatrixd(ravel(m)) #from Numeric...
      glMultMatrixd(m)
    self.wxRedraw()
    self.wxRecordMouse(event)

  def wxTranslate(self, event):
    """Perform translation of scene."""

    # Scale mouse translations to object viewplane so object tracks with mouse
    win_height = max( 1,self.w)
    obj_c      = (self.xcenter, self.ycenter, self.zcenter)
    win        = gluProject( obj_c[0], obj_c[1], obj_c[2] )
    obj        = gluUnProject( win[0], win[1] + 0.5 * win_height, win[2] )
    dist       = math.sqrt( v3distsq( obj, obj_c ) )
    scale      = abs( dist / ( 0.5 * win_height ) )

    glTranslateScene(scale, event.GetX(), event.GetY(), self.xmouse, self.ymouse)
    self.wxRedraw()
    self.wxRecordMouse(event)

  def wxRedrawGL(self, event=None):
    """Method used to actually draw the scene.

    This is more complex than in the wxGLWindow class from which this
    class is derived, as we need to do rotations, translations, etc."""
    self.SetCurrent()
    if self.GL_uninitialised:
      glViewport(0, 0, self.w, self.h)
      self.InitGL()
      self.GL_uninitialised = 0

    # Clear the background and depth buffer.
    glClearColor(self.r_back, self.g_back, self.b_back, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION);
    glLoadIdentity()
    gluPerspective(self.fovy, float(self.w)/float(self.h), self.near, self.far)

    gluLookAt(self.xcenter, self.ycenter, self.zcenter + self.distance,
              self.xcenter, self.ycenter, self.zcenter,
              0., 1., 0.)
    glMatrixMode(GL_MODELVIEW);

    glPushMatrix();
    self.DrawGL()           # Actually draw here
    glPopMatrix();
    glFlush()                           # Tidy up
    self.SwapBuffers()

    if event: event.Skip()


#-----------------------------------------------------

if __name__ == '__main__':
  from OpenGL.GLUT import *
  import array #for creating the texture map

  class MyApp(App):
    def OnInit(self):
      frame = Frame(None, -1, "wxPython OpenGL example", DefaultPosition, Size(400,400))
      #win1 = wxGLWindow(frame, -1, Point(5,5), Size(190,190))
      #win2 = wxAdvancedGLWindow(frame, -1, Point(205,5), Size(190,190), autospin_allowed = 0)
      win3 = MyWin1_1(frame, -1, Point(5,205), Size(190,190), autospin_allowed = 0)
      #win4 = MyWin2(frame, -1, Point(205,205), Size(190,190))
#      win1.SetScrollbars(0,0,0,0)
#      win4.SetScrollbars(0,0,0,0)
#      win3.SetBgColour(0.0,0.0,1.0)
      frame.Show(True)
      self.SetTopWindow(frame)
      return True
	  
  class MyWin1(wxAdvancedGLWindow):
    """basic example of a wxAdvancedGLWindow"""
    def DrawGL(self):
      glColor3f(1.0,0.3,0.3)
      glutSolidCone(1.0,2,20,16)
      glRotatef(180.0,0.0,1.0,0.0)
      glColor3f(0.3,1.0,0.3)
      glutSolidCone(1.0,1,20,16)
      glLoadIdentity()
  
  class MyWin1_1(wxAdvancedGLWindow):
    """basic example of a wxAdvancedGLWindow with basic triangles"""
    def InitGL(self):
        self.points,self.polylist=test_data(1000)
        print self.points, self.polylist
		
    def DrawGL(self):
        glColor4f(.1,.7,.7, 0.5)
        for p in self.polylist:
                if len(p)==3:
                    p0=self.points[p[0]]
                    p1=self.points[p[1]]
                    p2=self.points[p[2]]
                    glBegin(GL_TRIANGLES) #Drawing Using Triangles
                    glVertex3f( p0[0], p0[1], p0[2])
                    glVertex3f( p1[0], p1[1], p1[2])
                    glVertex3f( p2[0], p2[1], p2[2])
                    glEnd()     
       
  class MyWin2(wxAdvancedGLWindow):
    """example using display lists"""
    def InitGL(self):
      self.uninitialised = 1
      glClearColor (0.0, 0.0, 0.0, 0.0);
      glEnable(GL_DEPTH_TEST);
      glShadeModel(GL_SMOOTH);
      self.stripeImageWidth=32
      temp = array.array('B')
      for x in range(5):
        temp.fromlist([255,0,0,255])
      for x in range(self.stripeImageWidth-5):
        temp.fromlist([0,255,0,255])

      self.stripeImage = temp.tostring()
      glPixelStorei(GL_UNPACK_ALIGNMENT, 1);

      self.texName=glGenTextures(1)
      glBindTexture(GL_TEXTURE_2D, self.texName)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.stripeImageWidth,1,0,
                   GL_RGBA, GL_UNSIGNED_BYTE, [self.stripeImage])
      glTexImage2D(GL_TEXTURE_2D, 0, 4, self.stripeImageWidth, 1, 0,
                   GL_RGBA, GL_UNSIGNED_BYTE, [self.stripeImage])

      glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
      glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_EYE_LINEAR)
      glTexGenfv(GL_S, GL_EYE_PLANE, [1.0, 1.0, 1.0, 0.0])

      glEnable(GL_TEXTURE_GEN_S);
      glEnable(GL_TEXTURE_2D);
      glEnable(GL_CULL_FACE);
      glEnable(GL_LIGHTING);
      glEnable(GL_LIGHT0);
      glEnable(GL_AUTO_NORMAL);
      glEnable(GL_NORMALIZE);
      glFrontFace(GL_CW);
      glCullFace(GL_BACK);
      glMaterialf (GL_FRONT, GL_SHININESS, 64.0);
      self.DispList=glGenLists(1)

    def DrawGL(self):
      if self.uninitialised:
        glNewList(self.DispList, GL_COMPILE)
        glRotatef(45.0, 0.0, 0.0, 1.0);
        glBindTexture(GL_TEXTURE_2D, self.texName);
        glutSolidTeapot(2.0);
        glEndList()
        self.uninitialised = 0

      glCallList(self.DispList)
    def FinishGL(self):
      if self.DispList:
        glDeleteLists(self.DispList)

  app = MyApp(0)
  app.MainLoop()




