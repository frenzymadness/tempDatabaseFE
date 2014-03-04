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
    '/last/(.+)', 'last',
    '/averages/', 'averages',
    '/photos/', 'photos',
    '/photos/(.+)', 'photos'
    )

########################################################################


# Uvodni stranka s poslednim merenim
class index:

    def GET(self):
        # Posledni teplota pro kazdy sensor
        lasttemps = []
        result = db.query("SELECT DISTINCT position FROM records ORDER BY date, position DESC ;")
        for row in result:
            name = row['position']
            data = db.query('SELECT date, tempreature FROM records WHERE position = "%s" ORDER BY date DESC ' % (name)).list()
            serie = {'name': name, 'date': data[0]['date'], 'temp': data[0]['tempreature']}
            lasttemps.append(serie)

        # Zobrazeni posledni fotografie
        images = os.listdir(rootdir + 'static/images/')
        images.sort()
        lastimage = images[-1]

        return render.index(lasttemps, lastimage)


# Stranka nedavnou historii
class last:

    def GET(self, period=None):
    # filtrace zobrazenych hodnot dle url
        limit = ''
        where = ''
        if period == 'now' or period is None:
            limit = 'LIMIT 120'
            where = '1'
        if period == 'today':
            today = time.strftime('%Y-%m-%d') + ' %'
            where = 'date like "%s"' % (today)
        if period == 'yesterday':
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            yesterday = yesterday.strftime("%Y-%m-%d") + ' %'
            where = 'date like "%s"' % (yesterday)
        if period == 'week':
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

        #Conditions
        cond_serie = []
        data = db.query('select condition, count(condition) as count from (select condition from records where condition != "Inside" and %s %s) group by condition;' % (where, limit))
        # data musi byt setrizena - proto prevod na list a trizeni
        for record in data:
            cond_serie.append([record['condition'], record['count']])

        return render.last(json.dumps(temp_series), sensors, json.dumps(cond_serie))


class averages:
    def GET(self):
        tables = ['days', 'months', 'years']
        time_formats = ['%Y-%m-%d', '%Y-%m', '%Y']
        averages = []
        for index in xrange(len(tables)):
            averages.append({'table': tables[index], 'data': []})
            # Vybereme vsechny cidla z databaze a vytvorime serii pro kazde z nich
            result = db.query("SELECT DISTINCT position FROM %s ORDER BY date, position DESC;" % (tables[index]))
            for row in result:
                name = row['position']
                # Zakladni struktura kazde serie
                serie = {"name": name, "data": []}
                # vybereme data jen pro konkretni senzor
                data = db.query('SELECT date, tempreature FROM %s WHERE position = "%s" ORDER BY date DESC' % (tables[index], name))
                # data musi byt setrizena - proto prevod na list a trizeni
                for record in reversed(data.list()):
                    serie["data"].append([int(datetime.datetime.strptime(record['date'], time_formats[index]).strftime('%s')) * 1000, record['tempreature']])
                averages[index]["data"].append(serie)
            averages[index]['data'] = json.dumps(averages[index]['data'])
        return render.averages(averages)


class photos:
    """Zaznamy starych fotografii"""
    def GET(self, date=None):
        if date is None:
            return render.photos()
        else:
            files = os.listdir(rootdir + 'static/images/')
            images = [image for image in files if image.startswith(date)]
            return json.dumps(images)

########################################################################

application = web.application(urls, globals(), autoreload=True).wsgifunc()
