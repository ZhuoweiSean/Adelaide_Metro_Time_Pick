import pandas as pd
from pathlib import Path
from typing import Tuple

class Railway:
    def __init__(self):
        self.route_dict=dict()

    def add_route(self, route):
        self.route_dict[(route.id, route.service_days)]=route

    def search_route(self,service_days:str, dpt_time:float, dpt_stop:str, arr_stop:str):
        """
        For each matching route, pick the last train before dpt_time and the next two after.
        Returns a concatenated DataFrame of candidates across all routes, sorted by departure.
        """
        for id, route in self.route_dict.items():
            if not route.is_relevant(service_days, dpt_stop, arr_stop):
                continue

            df=route.timetable_df[(route.timetable_df[dpt_stop] != -1) & (route.timetable_df[arr_stop] != -1)]

            after=df.loc[df[dpt_stop]>=dpt_time, [dpt_stop,arr_stop]].head(2)
            before=df.loc[df[dpt_stop]<dpt_time, [dpt_stop,arr_stop]].tail(1)
            result=pd.concat([before,after])
            print(result)

    def traverse(self):
        for id, route in self.route_dict.items():
            print(f'id = {id}, route = {route.stop_seq}\n')

class Route:
    def __init__(self,id:str, days:str, stop_seq:list, timetable_df:pd.DataFrame):
        self.id=id
        self.service_days=days
        self.stop_seq=stop_seq
        self.timetable_df=timetable_df

    def is_relevant(self,service_days:str,dpt:str, arr:str):
        if service_days != self.service_days:
            return False
        if dpt not in self.stop_seq:
            return False
        if arr not in self.stop_seq:
            return False
        if self.stop_seq.index(dpt)>= self.stop_seq.index(arr):
            return False
        
        return True


def parse_filename(file: Path) -> Tuple[str, str]:
    """
    Expect filenames like 'Direction__Mon_to_Fri.csv'.
    """
    # Drops extension
    stem = file.stem  # e.g., "Seaford__Mon_to_Fri"
    if "__" not in stem:
        raise ValueError(f"Filename not in 'Direction__ServiceDays.csv' format: {file.name}")
    
    direction, service_days = stem.split("__", maxsplit=1)

    return direction, service_days


if __name__=="__main__":
    metro=Railway()

    for csv_file in Path("./csv").glob("*.csv"):
        timetable_df=pd.read_csv(csv_file).iloc[:,1:]
        stop_seq=list(timetable_df.columns)

        direction, service_days = parse_filename(csv_file)

        new_route=Route(direction,service_days,stop_seq,timetable_df)
        metro.add_route(new_route)

    #metro.search_route("Mon_to_Fri", 18.26, "Adelaide", "Hallett_Cove")
    #metro.search_route("Mon_to_Fri", 18.26, "Hallett_Cove", "Adelaide")
    #metro.search_route("Sat_Sun_PH", 18.26, "Adelaide", "Hallett_Cove")
    #metro.search_route("Sat_Sun_PH", 18.26, "Hallett_Cove", "Adelaide")
    input_service_days="Mon_to_Fri" if input("Input the number for service days:\n1. Monday to Friday\n2. Saturday/Sunday/Public Holiday")=="1" else "Sat_Sun_PH"
    input_dpt_time=float(input('Input the departure time in the format of "hh.mm" (e.g. 16.25 for 4:25 pm)'))
    input_dpt_stop=input("Input the name of departure stop")
    input_arr_stop=input("Input the name of arrival stop")

    metro.search_route(input_service_days,input_dpt_time,input_dpt_stop,input_arr_stop)