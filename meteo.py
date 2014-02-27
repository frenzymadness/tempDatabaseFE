import web
import os
import sys
import json
import datetime
import time

# pridani cesty ke knihovnam
lib_path = os.path.abspath('./libs')
sys.path.append(lib_path)

########################################################################
rootdir = os.path.abspath(os.path.dirname(__file__)) + '/'
render = web.template.render(rootdir + 'templates/',
                             base='layout', cache=False)

db = web.database(dbn='sqlite', db=rootdir + 'database/database.sqlite')

urls = (
    '/', 'index',
    '/last/(.+)', 'index',
    '/photos/', 'photos'
    )

########################################################################


# Stranka s poslednim merenim
class index:

    def GET(self, filter=None):
    # filtrace zobrazenych hodnot dle url
        limit = ''
        where = ''
        if filter == 'now' or filter is None:
            limit = 'LIMIT 120'
            where = '1'
        if filter == 'today':
            today = time.strftime('%Y-%m-%d') + ' %'
            where = 'date like "%s"' % (today)
        if filter == 'yesterday':
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            yesterday = yesterday.strftime("%Y-%m-%d") + ' %'
            where = 'date like "%s"' % (yesterday)
        if filter == 'week':
            today = time.strftime('%Y-%m-%d') + ' 23:59:59'
            weekback = datetime.date.today() - datetime.timedelta(days=7)
            weekback = weekback.strftime("%Y-%m-%d") + ' 00:00:00'
            where = 'date between "%s" and "%s"' % (weekback, today)

        # Prazdne pole pro serie dat grafu a maxima a minima senzeoru
        temp_series = []
        sensors = []
        # Vybereme vsechny cidla z databaze a vytvorime serii pro kazde z nich
        result = db.query("SELECT DISTINCT position FROM records WHERE %s ORDER BY date, position DESC %s;" % (where, limit))
        for row in result:
            name = row['position']
            # Zakladni struktura kazde serie
            serie = {'name': name, 'data': []}
            sensor = {'name': name, 'min': 1000, 'max': -1000}
            # vybereme data jen pro konkretni senzor
            data = db.query('SELECT date, tempreature FROM records WHERE position = "%s" and %s ORDER BY date DESC %s' % (name, where, limit))
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

        # Posledni hodnoty
        lasttemps = []
        for serie in temp_series:
            lasttemps.append({'name': serie['name'], 'temp': serie['data'][-1][1]})

        # Zobrazeni posledni fotografie
        images = os.listdir(rootdir + 'static/images/')
        images.sort()
        lastimage = images[-1]

        #Conditions
        cond_serie = []
        data = db.query('select condition, count(condition) as count from (select condition from records where condition != "Inside" and %s %s) group by condition;' % (where, limit))
        # data musi byt setrizena - proto prevod na list a trizeni
        for record in data:
            cond_serie.append([record['condition'], record['count']])

        return render.index(lasttemps, json.dumps(temp_series), lastimage, sensors, json.dumps(cond_serie))


class photos:
    """Zaznamy starych fotografii"""
    def GET(self):
        return render.photos()

########################################################################

application = web.application(urls, globals(), autoreload=True).wsgifunc()
