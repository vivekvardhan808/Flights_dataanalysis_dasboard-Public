import pymysql

class DB:

    def __init__(self):
        
        try:
            self.conn = pymysql.connect(
                host = '127.0.0.1',
                user = 'root',
                password = '1234',
                database = 'project'
            )

            self.mycursor = self.conn.cursor()

            print('Connection Established')
        except:
            print('Connection Not Established')

    # check Flights Page
    def fetch_city_names_s(self):

        city = []
        self.mycursor.execute("""
        SELECT distinct(source_city) FROM project.flights
        """)
        data = self.mycursor.fetchall()
        
        #print(data)
        for item in data:
            city.append(item[0])
        return city
    
    def fetch_city_names_d(self):

        city = []
        self.mycursor.execute("""
        SELECT distinct(destination_city) FROM project.flights
        """)
        data = self.mycursor.fetchall()
        
        #print(data)
        for item in data:
            city.append(item[0])
        return city
    
    def fetch_all_fights(self,Source,Destination):
        self.mycursor.execute(f"""
        SELECT airline,class,count(*),round(avg(price),2) as price
                                FROM project.flights
                                where source_city="{Source}" and destination_city = "{Destination}"
                                group by airline,class
                                order by price
        """)

        data = self.mycursor.fetchall()
        return data

    def count_of_fights(self,Source,Destination):
        count_flights = []
        self.mycursor.execute(f"""
        SELECT count(*) 
                                FROM project.flights
                                where source_city="{Source}" and destination_city = "{Destination}"
                                group by airline,class;

        """)

        data = self.mycursor.fetchall()
        for item in data:
            count_flights = item[0]

        return count_flights
    
    # Analytics Page    
    def fetch_airline_frequency(self):
        flights = []
        frequency = []
        self.mycursor.execute("""
        SELECT airline,count(*) as freq FROM project.flights
        group by airline
        order by freq desc                      
        """)
        data = self.mycursor.fetchall()
        for item in data:
            flights.append(item[0])
            frequency.append(item[1])

        return flights,frequency
    
    def fetch_airport_frequency(self):
        airport = []
        frequency = []
        self.mycursor.execute("""
        select source_city,count(*) as freq from(select source_city from project.flights
                                                union all
                                                select destination_city from project.flights) t
        group by t.source_city
        order by freq desc   
        """)
        data = self.mycursor.fetchall()
        for item in data:
            airport.append(item[0])
            frequency.append(item[1])

        return airport,frequency
    
    def fetch_avg_price_by_airline(self):
        airline = []
        price = []
        self.mycursor.execute("""
        SELECT airline,avg(price) as price FROM project.flights
        where class = 'Economy'
        group by airline
        order by price   
        """)
        data = self.mycursor.fetchall()
        for item in data:
            airline.append(item[0])
            price.append(item[1])

        return airline,price
    
    # fetching about the no.of fights at source and destination

    def fetch_count_of_flights_destination(self):
        city = []
        count = []
        self.mycursor.execute("""
        select destination_city,count(*) from project.flights
        group by destination_city
        order by destination_city   
        """)
        data = self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
            count.append(item[1])

        return city,count
    
    def fetch_count_of_flights_source(self):
        city = []
        count = []
        self.mycursor.execute("""
        select source_city,count(*) from project.flights
        group by source_city
        order by source_city   
        """)
        data = self.mycursor.fetchall()
        for item in data:
            city.append(item[0])
            count.append(item[1])

        return city,count

    def fetch_price_vs_dep_time(self):
        
        self.mycursor.execute("""
        SELECT departure_time,airline,round(avg(price)) as price FROM project.flights
        where class = 'Economy'
        group by departure_time,airline  
        """)
        data = self.mycursor.fetchall()

        return data