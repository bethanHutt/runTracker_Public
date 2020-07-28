
class Run():
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            if isinstance(val, str) and val.isdigit():
                self.__dict__[key] = float(val)
            else:    
                self.__dict__[key] = val

    @property
    def adjusted_speed(self):
        #kilometers per hour
        adjusted_speed = (self.distance / self.time) * 3600
        return adjusted_speed
    
    @property
    def adjusted_pace(self):
        #minutes per kilometer
        adjusted_pace = 60 / self.adjusted_speed
        return adjusted_pace
