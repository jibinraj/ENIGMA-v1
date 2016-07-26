import wx
import wx.xrc


import datetime
import os 
import threading
import time
import os.path


index=0
flag=0
flag1=0
selfg=""

class const():
    sourcelist=[]
    filelist=[]
    sizelist=[]
    filesize=[]
class tmp():
    files=[]
    total=0
    sizes=[]
    source=""
    target=""
    paths=[]
    pathd=[]

class clock():
    start_time=0

class pack():
    size1=0
    size2=0
    size3=0
    data=[[],[]]


class read_data(threading.Thread) :
    def run (self):
##        print "read"
        global flag
        r=1
        while len(tmp.files)>0 or len(tmp.paths)>0:
####            if len(tmp.files)>0 :
####                selfg.filfo()
######                del tmp.files[0]
            if flag !=2 and len(tmp.paths)>0:
                if r==1 :
                    r=0
                elif r==0:
                    r=1
                pack.size1=0
                ##print "READING:",tmp.paths
                f1=open(tmp.paths[0],'rb')
                a="1"
                while a!="":
##                    print "reading"
                    if (pack.size1+10000000)<tmp.total :
                        a=f1.read(10000000)
                        pack.data[r].append(a)
                        pack.size1+=len(a)
                    else :
                        a=f1.read()
                        pack.data[r].append(a)
                        pack.size1+=len(a)
##                print "read_finished:",tmp.paths
                flag+=1
##                print len(tmp.files),";",len(tmp.pathd)
                del tmp.paths[0]
                if len(tmp.files)>0 :
                    del tmp.files[0]
                f1.close()
            

        
class write_data(threading.Thread) :
    def run (self) :
##        print "write"
        global rd_trd
        global flag
        global flag1
        global selfg
        w=1
        ##time.sleep(1)
        ##print "WRITING:",tmp.pathd
        ##time.sleep(1)
        
        while rd_trd.is_alive() or len(tmp.pathd)>0  :
            if len(tmp.pathd)>0 :
                if w==1:
                    w=0
                elif w==0 :
                    w=1
                pack.size2=0
                pack.size3=0
    ##            while len(tmp.pathd)==0 and rd_trd.is_alive() :
    ##                print "wait"
                f2=open(tmp.pathd[0],'wb')
               ## print tmp.pathd[0],"---writing"
                while len(pack.data[w])>0 or flag==0:
                    if len(pack.data[w])>0 :
##                        print "writing"
                        f2.write(pack.data[w][0])
                        pack.size2+=len(pack.data[w][0])
                        pack.size3+=len(pack.data[w][0])
                        del pack.data[w][0]
                f2.close()
##                print "writing finished",tmp.pathd
                del tmp.pathd[0]
                flag-=1
                flag1=1
#####################################
        ##del tmp.sizes[0]
        
        #############################
        print " WRITE finished:"






################################
class f_path(threading.Thread) :
    def run (self) :
        global selfg
        self.files=tmp.files
        while len(self.files)>0 :
            self.files=tmp.files
            selfg.filfo()
            del self.files[0]
        

##################################




class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
    def OnDropFiles(self,x,y,filenames):
        global i
        b=[]
        i=0
        totalsize=0
        path,name=os.path.split ( filenames[0] )
        i+=1
        self.window.AppendText("%d--%s\n"%(i,path))
        const.filelist.append(filenames)
        for file in filenames:    
            path,name=os.path.split ( file )
            if os.path.isdir(file):
                a=self.calc(file)
            else :
                a=os.path.getsize(file)
            b.append(a)
            totalsize=totalsize+a
            self.window.AppendText ("\t%s-%s\n" % (name,self.size_conv(a)) )
        const.sourcelist.append(path)
        i+=1
        const.sizelist.append(totalsize)
        const.filesize.append(b)
        self.window.AppendText("\t\t\tTotal=%s\n"%(self.size_conv(totalsize)) )
        self.window.AppendText("______________________________________________________________________\n")
        #print const.sizelist
        #print const.filelist
        #print const.filesize
        #print const.sourcelist
    def calc(self,path) :
        size=0
        for item in os.listdir(path) :
            if os.path.isdir(path+os.sep+item) :
                b=self.calc(path+os.sep+item)
            else :
                b=os.path.getsize(path+os.sep+item)
            size=size+b
        return size
    def size_conv(self,size) :
        if size < 1024:
            return str(size)+" B"
        elif size/1024 < 1024 :
            size=size/1024.0
            s=str(size)
            if '.' in s :
                i=str(size).index('.')+3
                s=s[:i]
            return s+" KB"
        elif size/(1024*1024) <1024 :
            size=size/(1024*1024.0)
            s=str(size)
            print "ds"
            if '.' in s :
                print "mb"
                i=str(size).index('.')+3
                s=s[:i]
            return s+" MB"
        else:
            size=size/(1024*1024*1024.0)
            s=str(size)
            if '.' in s :
                i=str(size).index('.')+3
                s=s[:i]
            return s+" GB" 
        

###########################################################################
## Class frame1
###########################################################################

class frame1 ( wx.Frame ):
	
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTIONTEXT ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNHIGHLIGHT ) )
        
        bsizer1 = wx.BoxSizer( wx.VERTICAL )
        
        self.statictext1 = wx.StaticText( self, wx.ID_ANY, u"File List", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
        self.statictext1.Wrap( -1 )
        self.statictext1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
        self.statictext1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
        
        bsizer1.Add( self.statictext1, 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
        
        self.textctrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
        bsizer1.Add( self.textctrl1, 1, wx.EXPAND, 5 )
        
        self.copybut = wx.Button( self, wx.ID_ANY, u"COPY", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
        bsizer1.Add( self.copybut, 0, wx.EXPAND, 5 )
        
        
        self.SetSizer( bsizer1 )
        self.Layout()
        self.statusbar = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
        self.menubar = wx.MenuBar( 0 )
        self.menu1 = wx.Menu()
        self.menuitem11 = wx.MenuItem( self.menu1, wx.ID_ANY, u"MyMenuItem", wx.EmptyString, wx.ITEM_NORMAL )
        self.menu1.AppendItem( self.menuitem11 )
        
        self.submenu11 = wx.Menu()
        self.menu1.AppendSubMenu( self.submenu11, u"MyMenu" )
        
        self.menubar.Append( self.menu1, u"MyMenu" ) 
        
        self.menu2 = wx.Menu()
        self.menubar.Append( self.menu2, u"MyMenu" ) 
        
        self.SetMenuBar( self.menubar )
        
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.copybut.Bind( wx.EVT_BUTTON, self.copy )

        dt = MyFileDropTarget(self.textctrl1)
        self.textctrl1.SetDropTarget(dt)
        self.Show()
    
    def __del__( self ):
        self.Destroy()
        
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def copy( self, event ):
####******************************************************************************************************
        frame2(self)
        event.Skip()




class frame2 ( wx.Frame ):
	
    def __init__( self, parent ):
        
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Browse", pos = wx.DefaultPosition, size = wx.Size( 400,240 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.Size( 400,240 ), wx.Size( 400,240 ) )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        
        vbox1 = wx.BoxSizer( wx.VERTICAL )
        
        self.stext1 = wx.StaticText( self, wx.ID_ANY, u"name", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stext1.Wrap( -1 )
        vbox1.Add( self.stext1, 0, wx.ALIGN_CENTER|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
        
        self.sline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        vbox1.Add( self.sline1, 0, wx.EXPAND|wx.ALL, 5 )
        
        hbox1 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.stext2 = wx.StaticText( self, wx.ID_ANY, u"size", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stext2.Wrap( -1 )
        hbox1.Add( self.stext2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL, 5 )
        
        self.notext1 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.notext1.Wrap( -1 )
        hbox1.Add( self.notext1, 1, wx.ALL, 5 )
        
        self.stext3 = wx.StaticText( self, wx.ID_ANY, u"num", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.stext3.Wrap( -1 )
        hbox1.Add( self.stext3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.notext2 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.notext2.Wrap( -1 )
        hbox1.Add( self.notext2, 1, wx.ALL, 5 )
        
        self.bdeta = wx.Button( self, wx.ID_ANY, u"Details>>", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.bdeta.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
        self.bdeta.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOTEXT ) )
        
        hbox1.Add( self.bdeta, 0, wx.ALIGN_CENTER_VERTICAL, 5 )
        
        
        vbox1.Add( hbox1, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND, 5 )
        
        self.sline = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        vbox1.Add( self.sline, 0, wx.EXPAND |wx.ALL, 5 )
        
        self.dirpick = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_CHANGE_DIR|wx.DIRP_DEFAULT_STYLE|wx.TAB_TRAVERSAL )
        vbox1.Add( self.dirpick, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 5 )
        
        hbox2 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.skip = wx.Button( self, wx.ID_ANY, u"skip", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
        hbox2.Add( self.skip, 1, wx.ALIGN_LEFT|wx.ALL, 5 )
        
        self.copy = wx.Button( self, wx.ID_ANY, u"start copy", wx.DefaultPosition, wx.DefaultSize, 0 )
        hbox2.Add( self.copy, 1, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        self.cancel = wx.Button( self, wx.ID_ANY, u"cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        hbox2.Add( self.cancel, 1, wx.ALL, 5 )
        
        
        vbox1.Add( hbox2, 1, wx.EXPAND, 5 )
        
        
        self.SetSizer( vbox1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        #***********************************************************************************
        global index
        tmp.tempfiles=[]
        tmp.indsize=[]
        tmp.totalsize=0
        self.files=const.filelist[index]
        self.size=const.sizelist[index]
        self.stext1.SetLabel(os.path.split(self.files[0])[1])
        self.stext2.SetLabel(str(self.size))
        self.stext3.SetLabel(str(len(self.files)))
        self.Show(True)
        # Connect Events
        self.skip.Bind( wx.EVT_BUTTON, self.skip1 )
        self.copy.Bind( wx.EVT_BUTTON, self.start_copy )
        self.cancel.Bind( wx.EVT_BUTTON, self.cancel1 )
        self.dirpick.Bind( wx.EVT_DIRPICKER_CHANGED, self.target_set )


    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def skip1( self, event ):
        global index
        if((index+1)==len(const.filelist)):
            index=0
            self.Show(False)
            self.Destroy()
        else :
            index+=1
            self.Show(False)
            self.Destroy()
            frame2(self.GetParent())
        event.Skip()
        
    
    def start_copy( self, event ):
        if tmp.target!="":
            self.Show(False)
            self.Destroy()
            tmp.files=const.filelist[index]
            tmp.sizes=const.filesize[index]
            tmp.total=const.sizelist[index]
            tmp.source=const.sourcelist[index]
            #tmp.tmpfiles
            frame3(self.GetParent())
        event.Skip()
    
    def cancel1( self, event ):
        self.Show(False)
        self.Destroy()
        global index
        index=0
        event.Skip()

    def target_set ( self,event ):
        tmp.target=self.dirpick.GetPath ( )
        pass


###########################################################################
## Class frame3
###########################################################################

class frame3 ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"File Transporter", pos = wx.DefaultPosition, size = wx.Size( 450,250 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.CLIP_CHILDREN|wx.STATIC_BORDER|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.Size( 450,250 ), wx.Size( 450,250 ) )
        self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
        
        vbox1 = wx.BoxSizer( wx.VERTICAL )
        
        bsizer1 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.statictext1 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.statictext1.Wrap( -1 )
        self.statictext1.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 71, 90, 92, False, "Levenim MT" ) )
        
        bsizer1.Add( self.statictext1, 0, wx.ALIGN_LEFT|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.statictext2 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.statictext2.Wrap( -1 )
        bsizer1.Add( self.statictext2, 1, wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        self.statictext3 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.statictext3.Wrap( -1 )
        self.statictext3.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 71, 90, 92, False, "Levenim MT" ) )
        
        bsizer1.Add( self.statictext3, 0, wx.ALIGN_RIGHT|wx.TOP|wx.RIGHT|wx.LEFT, 5 )
        
        
        vbox1.Add( bsizer1, 1, wx.EXPAND, 5 )
        
        self.gauge1 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( -1,-1 ), wx.GA_HORIZONTAL|wx.GA_SMOOTH )
        self.gauge1.SetValue( 0 ) 
        vbox1.Add( self.gauge1, 0, wx.EXPAND|wx.ALL, 5 )
        
        bsizer2 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.statictext4 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.statictext4.Wrap( -1 )
        self.statictext4.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 71, 90, 92, False, "Levenim MT" ) )
        
        bsizer2.Add( self.statictext4, 0, wx.ALIGN_LEFT|wx.ALL, 5 )
        
        self.statictext5 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.statictext5.Wrap( -1 )
        bsizer2.Add( self.statictext5, 1, wx.ALL, 5 )
        
        self.statictext6 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.statictext6.Wrap( -1 )
        self.statictext6.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 71, 90, 92, False, "Levenim MT" ) )
        
        bsizer2.Add( self.statictext6, 0, wx.ALL, 5 )
        
        
        vbox1.Add( bsizer2, 1, wx.EXPAND, 5 )
        
        self.gauge2 = wx.Gauge( self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.gauge2.SetValue( 0 ) 
        vbox1.Add( self.gauge2, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.statictext7 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.statictext7.Wrap( -1 )
        self.statictext7.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 71, 90, 92, False, "Levenim MT" ) )
        
        vbox1.Add( self.statictext7, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        gridbox1 = wx.GridSizer( 0, 3, 0, 5 )
        
        self.pause = wx.Button( self, wx.ID_ANY, u"Pause", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.pause.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )
        
        gridbox1.Add( self.pause, 0, wx.BOTTOM|wx.LEFT|wx.TOP, 5 )
        
        self.skip = wx.Button( self, wx.ID_ANY, u"Skip", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.skip.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        
        gridbox1.Add( self.skip, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        self.cancel = wx.Button( self, wx.ID_ANY, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cancel.SetBackgroundColour( wx.Colour( 253, 2, 21 ) )
        
        gridbox1.Add( self.cancel, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM|wx.LEFT|wx.TOP, 5 )
        
        
        vbox1.Add( gridbox1, 0, wx.EXPAND, 5 )
        
        
        self.SetSizer( vbox1 )
        self.Layout()
        self.statusbar = self.CreateStatusBar( 3, 0, wx.ID_ANY )
        self.statusbar.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.Bind( wx.EVT_CLOSE, self.onf1close )
        self.statictext1.Bind( wx.EVT_ENTER_WINDOW, self.enter1 )
        self.statictext4.Bind( wx.EVT_ENTER_WINDOW, self.enter2 )
        self.pause.Bind( wx.EVT_LEFT_DOWN, self.pause_but_1 )
        self.skip.Bind( wx.EVT_LEFT_DOWN, self.skip_but_1 )
        self.cancel.Bind( wx.EVT_LEFT_DOWN, self.cancel_but_1 )
        self.Bind(wx.EVT_IDLE, self.update )
#qwertyuiopasdfghjklzxcvbnm
        global index
        ################################
        global selfg
        selfg=self
        ###################################################
##        self.totalsize=tmp.totalsize
##        self.file=tmp.tempfiles
##        self.size=tmp.indsize
        self.target=tmp.target
        self.source=tmp.source
##        self.filfo()
        self.statictext6.SetLabel(str(tmp.total))
        self.statictext4.SetLabel(os.path.split(tmp.files[0])[0])
        self.Show(True)
        ##self.filfo()
        self.rd_wr()
        

    def __del__( self ):
            pass
    
    
    # Virtual event handlers, overide them in your derived class
    def filfo(self) :
##        print "filefo:",len(tmp.files)
        if os.path.isdir(tmp.files[0]) :
            self._folder(tmp.files[0])
        else :
            self._file(tmp.files[0])
            
    def _folder(self,fol) :
##        print "folder"
        tar=self.splitpath(fol)
##        print tar
        path1=tmp.target+os.sep+tar
        if os.path.isdir(path1):
            pass
        else :
            os.mkdir(path1)
        _list=os.listdir(fol)
        del tmp.files[0]
        for item in _list :
##            print item
            item=fol+os.sep+item
            tmp.files.insert(0,item)
            tmp.sizes.insert(0,os.path.getsize(item))
##        print tmp.files
        self.filfo()
        
            
    def _file(self,fil) :
##        print "file"
        tar=self.splitpath(fil)
##        print "paths=",fil
##        print "pathd=",tmp.target+os.sep+tar
        tmp.paths.append(fil)
        tmp.pathd.append(tmp.target+os.sep+tar)

    def splitpath(self,path) :
        tar=""
        self.source=self.source.replace('//','/')
        path1,path2=os.path.split(path)
        path1=path1.replace('//','/')
        tar=path2
        while path1!=self.source :
            path1,path2=os.path.split(path1)
            tar=path2+os.sep+tar
            path1=path1.replace('//','/')
##            print tar
        return tar


    def rd_wr(self) :
        global rd_trd
        global wt_trd
        self.path=f_path()
        self.path.start()
        self.trdr=read_data()
        self.trdr.start()
        clock.start_time=datetime.datetime.now()
        print clock.start_time
        rd_trd=self.trdr
        self.trdw=write_data()
        self.trdw.start()
        wt_trd=self.trdw

    def onf1close( self, event ):
            
            event.Skip()
    
    def enter1( self, event ):
            event.Skip()
    
    def enter2( self, event ):
            event.Skip()
    
    def pause_but_1( self, event ):
            event.Skip()
    
    def skip_but_1( self, event ):
            event.Skip()
    
    def cancel_but_1( self, event ):
            event.Skip()

    def update(self,event):
        global end_time
        global j
        global rd_trd
        global wt_trd
        global flag1
        if flag1==0:
            if tmp.sizes[0]==0:
                tmp.sizes[0]=1
            step1=(pack.size3*100.0)/tmp.total
            step2=(pack.size2*100.0)/tmp.sizes[0]
            self.gauge1.SetValue(step2)
            self.gauge2.SetValue(step1)
            self.statusbar.SetStatusText(str("{0:.3}%".format(step1)),1)
            self.statictext7.SetLabel("{0:.3}%".format(step1))
            self.Update()
            end_time=datetime.datetime.now()
##            print "updating"
            ############################################
##            print "read:",(pack.size1*1.0),"-",(self.size[0]*1.0),"%"
        else :
            self.gauge1.SetValue(100)
            self.Update()
            print "exiting"
            flag1=0
            if (len(tmp.files)>0) or len(tmp.pathd)>0:
                self.statictext1.SetLabel(os.path.split(tmp.files[0])[1])
                self.statictext3.SetLabel(str(tmp.sizes[0]))
            else :
               wt_trd.TerminateProcess()
               self.Show(False)
               self.Destroy()
                
        event.Skip()



app=wx.App()
frame1(None)
app.MainLoop()
