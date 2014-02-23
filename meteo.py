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
    # Prazdne pole pro serie dat grafu a maxima a minima senzeoru
    temp_series = []
    sensors = []
    # Vybereme vsechny cidla z databaze a vytvorime serii pro kazde z nich
    result = db.query("SELECT DISTINCT position FROM records ORDER BY date, position DESC LIMIT 120;")
    for row in result:
      name = row['position']
      # Zakladni struktura kazde serie
      serie = {'name': name, 'data':[]}
      sensor = {'name': name, 'min': 1000, 'max': -1000}
      # vybereme data jen pro konkretni senzor
      data = db.select('records', what="date,tempreature", where='position = $position', vars={'position':name}, order="date DESC", limit=120)
      # data musi byt setrizena - proto prevod na list a trizeni
      for record in reversed(data.list()):
        serie['data'].append([int(datetime.datetime.strptime(record['date'], "%Y-%m-%d %H:%M:%S").strftime('%s')) * 1000, record['tempreature']])
        # Hledani maxim a minim
        if record['tempreature'] < sensor['min']:
          sensor['min'] = record['tempreature'] 
        if record['tempreature'] > sensor['max']:
          sensor['max'] = record['tempreature'] 
      temp_series.append(serie)
      sensors.append(sensor)

    # Zobrazeni posledni fotografie
    images = os.listdir(rootdir + 'static/images/')
    images.sort()
    lastimage = images[-1]

    #Conditions
    cond_serie = []
    data = db.query('select condition, count(condition) as count from (select condition from records where condition != "Inside" limit 120) group by condition;')
    # data musi byt setrizena - proto prevod na list a trizeni
    for record in data:
      cond_serie.append([record['condition'], record['count']])

    return render.index(json.dumps(temp_series), lastimage, sensors, json.dumps(cond_serie))

########################################################################
    
application = web.application(urls, globals(), autoreload=True).wsgifunc()  
