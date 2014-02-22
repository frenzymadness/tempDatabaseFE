import web
import os
import sys

# pridani cesty ke knihovnam
lib_path = os.path.abspath('./libs')
sys.path.append(lib_path)

########################################################################
rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
render = web.template.render(rootdir + 'templates/', base='layout', cache=False)

urls = (
    '/', 'index'
)

########################################################################

# Hlavni stranka pro vyhledani a nahlaseni IP adresy
class index:
  def GET(self):
    return render.index()

########################################################################
    
application = web.application(urls, globals(), autoreload=True).wsgifunc()  
