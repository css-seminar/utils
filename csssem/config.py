from datetime import datetime
from datetime import date as dt
from datetime import timedelta
# UPDATE: update this each semester
REPO = 'http://css-seminar.github.io/'
BASE_URL = 'https://raw.githubusercontent.com/css-seminar/css-seminar.github.io/main'


GH_APPROVERS = ['brownsarahm']

def expand_range(first_day,last_day=None,days_of_week=[]):
    if last_day:
        # subtract and expand
        num_days = (last_day-first_day).days
        days_in_range = [first_day+timedelta(i) for i in range(num_days)]
        return [cd for cd in days_in_range if cd.weekday() in days_of_week]
    else: 
        return [first_day]

class CourseDates(): 
    # scheduling choice
    meeting_days =[4] # datetime has 0=Monday
    meeting_hour = 15 # cutoff to ttreat prev at this hour

    # -------semester settings from academic calender 
    #  https://web.uri.edu/academic-calendars/
    first_day = dt(2026,1,30)
    last_day = dt(2026,4,29)

    #  add any skipped days or ranges (without makeup)
    # single days must be  tuple, (have a ,)
    no_class_ranges = [(dt(2026,3,16),dt(2026,3,22)),]
    
    
                    #    (dt(2025,11,11),),
    # classes "cancelled" on keys, running on value instead
    date_substitutes = {dt(2026,2,16):dt(2026,2,18)}
    # instructor choices
    penalty_free_end = first_day + timedelta(days=21)
    early_bird_deadline = first_day + timedelta(days=21)
    def __init__(self):
        # set class days
        skipped_days = ([day for date_range in self.no_class_ranges for day in expand_range(*date_range
                                                                                            ,days_of_week=self.meeting_days)] +
                        list(self.date_substitutes.values() )  )
        
        possible_list = expand_range(self.first_day,self.last_day,self.meeting_days)
        # if not skipped, check if replaced otherwise use that date
        self.class_meetings = [self.date_substitutes.get(m,m) for m in possible_list 
                               if not(m in skipped_days)]
        self.class_meeting_strings = [m.isoformat() for m in self.class_meetings]

        # set lab days 
        possible_labs = expand_range(self.first_day,self.last_day,[self.lab_day])
        self.lab_meetings = [self.date_substitutes.get(m,m) for m in possible_labs 
                             if not(m in skipped_days)]
        self.lab_meeting_strings = [m.isoformat() for m in self.lab_meetings]
    

    def prev_class(self,today):
        # all before, then take the last one
        return [cd for cd in self.class_meetings if cd <= today][-1]

    def next_class (self,today):
        # all after, then take the first one
        return [cd for cd in self.class_meetings if cd > today][0]
    
