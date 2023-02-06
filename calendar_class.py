import sqlite3
from datetime import datetime
from datetime import timedelta
from pathlib import Path

class event:

    def __init__(self, event_name="Founded", date="9/3/2019", time="12:00 am", length=2) -> None:
        self.name = event_name
        self.start_date_time = parse_date_time(date, time)
        self.start_date = self.start_date_time.date()
        self.start_time = self.start_date_time.time()
        self.length = length
        self.end_date_time = self.start_date_time + timedelta(hours=length)
        self.end_date = self.end_date_time.date()
        self.end_time = self.end_date_time.time()

    def info_list_str(self):
        return [self.name, str(self.start_date), str(self.start_time), str(self.end_date), str(self.end_time), self.length]

    def __str__(self) -> str:
        return self.name + ": " + str(self.start_date) + " " + str(self.start_time) + " to " + str(self.end_date_time) + " length: " + str(self.length)

class calendar:

    def __init__(self, db_filename) -> None:

        if not Path("./" + db_filename).is_file(): # Check if file doesnt exists
            new_db_file = open(db_filename, "w") 
            new_db_file.close()

        self.__db_conn = sqlite3.connect(db_filename)
        self.__db_cur = self.__db_conn.cursor()
        sql_create_events_table = """
            CREATE TABLE IF NOT EXISTS events(
            id integer PRIMARY KEY,
            name text NOT NULL,
            start_date text NOT NULL,
            start_time text NOT NULL,
            end_date text NOT NULL,
            end_time text NOT NULL,
            length integer NOT NULL
            );
            """
        self.__db_cur.execute(sql_create_events_table)
        self.event_count = self.__db_cur.execute("SELECT COUNT(*) FROM events").fetchone()[0] # Get number of events already in database

        

    def create_event(self, event_name="I Joined", date="9/14/2020", time="1:15 pm", length=1):
        self.event_count += 1
        new_event = event(event_name, date, time, length)
        sql_cmd = "INSERT INTO events(id, name, start_date, start_time, end_date, end_time, length) VALUES(?,?,?,?,?,?,?)"
        
        self.__db_cur.execute(sql_cmd, [self.event_count] + new_event.info_list_str())
        self.__db_conn.commit()

    def delete_event(self):
        pass

    def make_image(self):
        pass

    def fetch_events(self):
        sql_cmd = "SELECT * FROM events"
        events = self.__db_cur.execute(sql_cmd).fetchall()
        return events

def parse_date_time(str_date, str_time):
    """
    Function combines a string date and time into a single datetime object
    """
    date = parse_date(str_date)
    time = parse_time(str_time) # Both are datetime objects
    combined_date_time = datetime.combine(date, time.time())
    return combined_date_time


def parse_time(str_time):
    """
    Function is used to parse times into a datetime object https://pubs.opengroup.org/onlinepubs/007904875/functions/strptime.html for info on formatting
    """
    time = None
    try:
        time = datetime.strptime(str_time, "%H:%M:%S")
    except ValueError:
        try:
            time = datetime.strptime(str_time, "%I:%M:%S %p")
        except ValueError:
            try:
                time = datetime.strptime(str_time, "%H:%M")
            except ValueError:
                try:
                    time = datetime.strptime(str_time, "%I:%M %p")
                except ValueError:
                    raise Exception("Unrecognized time format :(")
    return time

def parse_date(str_date):
    """
    Function is used to parse dates into a datetime object https://pubs.opengroup.org/onlinepubs/007904875/functions/strptime.html for info on formatting
    """
    date = None
    try:
        date = datetime.strptime(str_date, "%m/%d/%y")
    except ValueError:
        try:
            date = datetime.strptime(str_date, "%m/%d/%Y")
        except ValueError:
            try:
                date = datetime.strptime(str_date, "%m-%d-%y")
            except ValueError:
                try:
                    date = datetime.strptime(str_date, "%m-%d-%Y")
                except ValueError:
                    raise Exception("Unrecognized date format :(")
    return date

if __name__ == "__main__":
    print(parse_date("10-23-2022"))
    print(parse_time("9:30 am"))
    print(event(event_name="R6 Practice", date="2/14/2023", time="8:00 pm", length=2))

    my_cal = calendar("calendar.db")
    my_cal.create_event()
    my_cal.create_event(event_name="R6 Practice", date="2/14/2023", time="8:00 pm", length=2)
    print(my_cal.fetch_events())