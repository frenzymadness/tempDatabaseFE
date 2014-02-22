import web
import os
import sys
import json
import datetime

# pridani cesty ke knihovnam
lib_path = os.path.abspath('./libs')
sys.path.append(lib_path)

########################################################################
rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
render = web.template.render(rootdir + 'templates/', base='layout', cache=False)

db = web.database(dbn='sqlite', db=rootdir + 'database/database.sqlite')

urls = (
    '/', 'index'
)

########################################################################

# Hlavni stranka
class index:
  def GET(self):
    series = []
    result = db.query("SELECT DISTINCT position FROM records;")
    for row in result:
      name = row['position']
      serie = {'name': name, 'data':[]}
      data = db.select('records', what="date,tempreature", where='position = $position', vars={'position':name}, order="date DESC", limit=120)
      for record in reversed(data.list()):
        serie['data'].append([int(datetime.datetime.strptime(record['date'], "%Y-%m-%d %H:%M:%S").strftime('%s')) * 1000, record['tempreature']])
      series.append(serie)
    return render.index(json.dumps(series))

########################################################################
    
application = web.application(urls, globals(), autoreload=True).wsgifunc()  
