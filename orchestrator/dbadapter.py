import psycopg2

from logger import log

class DbAdapter:


    def __init__(self):
        self.LOG_TAG = "DBADAPTER"
        self.cur = None
        self.conn = None

        log(1, self.LOG_TAG, 'Initializing results database.')

        
        self.conn = psycopg2.connect(dbname="4yp_results", user="4yp", password="4yp", host="127.0.0.1", port=7001)
        self.cur = self.conn.cursor()
        self.cleanDatabase()

    def cleanDatabase(self, cleanParams = True):
        log(1, self.LOG_TAG, 'Cleaning databse to pure state.')
        self.cur.execute("DROP TABLE IF EXISTS file_results")
        self.cur.execute("DROP TABLE IF EXISTS overall_results")
        if cleanParams:
            self.cur.execute("DROP TABLE IF EXISTS parameters")

            log(1, self.LOG_TAG, 'Creating parameters table')
            self.cur.execute("""CREATE TABLE parameters (parameter_id serial PRIMARY KEY, filter text NOT NULL, scoring text NOT NULL, detection text NOT NULL, post text NOT NULL);""")

        log(1, self.LOG_TAG, 'Creating file_results table')
        self.cur.execute("""CREATE TABLE file_results (id serial PRIMARY KEY, phone text NOT NULL, person text NOT NULL, surface text NOT NULL, position text NOT NULL, accuracy real NOT NULL, parameters int NOT NULL REFERENCES parameters(parameter_id));""")

        log(1, self.LOG_TAG, 'Creating overall_results table')
        self.cur.execute("""CREATE TABLE overall_results (id serial PRIMARY KEY, parameters int NOT NULL REFERENCES parameters(parameter_id), accuracy real NOT NULL);""")

        self.conn.commit()

    def addEntry(self, result):

        acc = result['stats']['accuracy']
        param_id = result['algorithm']['params']['key']

        self.cur.execute("""INSERT INTO overall_results (parameters, accuracy) VALUES (%s, %s);""", (param_id,acc))

        for filename in result['results']:
            (phone, person, surface, position) = self.decodeFileName(filename)
            acc = result['results'][filename]['accuracy']
            self.cur.execute("""INSERT INTO file_results (phone, person, surface, position, accuracy, parameters) VALUES (%s,%s,%s,%s,%s,%s)""", (phone, person, surface, position, acc, param_id))

        self.conn.commit()
         

    def addParameterSet(self, params):

        sFilter = "/"
        sScoring = "/"
        sDetection = "/"
        sPost = "/"

        for key in params['filter']:
            sFilter += key + ":" + str(params['filter'][key]) + "/"
        for key in params['scoring']:
            sScoring += key + ":" + str(params['scoring'][key]) + "/"
        for key in params['detection']:
            sDetection += key + ":" + str(params['detection'][key]) + "/"
        for key in params['post']:
            sPost += key + ":" + str(params['post'][key]) + "/"

        self.cur.execute("""INSERT INTO parameters (filter, scoring, detection, post) VALUES(%s, %s, %s, %s) RETURNING parameter_id;""", (sFilter, sScoring, sDetection, sPost))
        p_key = self.cur.fetchone()[0]
        self.conn.commit()
        return p_key

    def getBest(self, number):

        self.cur.execute("""SELECT * FROM overall_results ORDER BY accuracy DESC LIMIT %s""", (number,))
        return self.cur.fetchall()


    def decodeFileName(self, filename):
        split = filename.split('_')
        return (split[0], split[1], split[2], split[3])