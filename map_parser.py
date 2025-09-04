import pandas as pd

def load_timetable(path:str):
    with open(path,"r") as f:
        rows=[]
        stop_id=[]
        for line in f:
            if line.startswith('Stop_names'):
                stop_id=line.strip().split(":")[1].split(", ")
                continue
            if line.startswith(('Direction','Service_days')):
                continue
            line=line.strip().replace('-','-1')
            if line:
                rows.append(line.split())
        df_raw=pd.DataFrame(rows,columns=stop_id, dtype=float)
        cross_midday_check(df_raw)
        save_name=path.split("/")[-1].split(".")[0]
        save_path="./csv/"+save_name+".csv"
        df_raw.to_csv(save_path)

    return df_raw

def cross_midday_check(df:pd.DataFrame):
    for col in df.columns:
        offset=0
        pre_val=5
        for idx, val in df[col].items():
            if val == -1:
                continue
            if val < pre_val:
                offset+=12 # convert to 24H display
            df.at[idx, col] = val + offset
            pre_val=val

def search(timetable:pd.DataFrame, dept_stop, dept_time,arrvl_stop):
    df=timetable[(timetable[dept_stop] != -1) & (timetable[arrvl_stop] != -1)]

    after=df.loc[df[dept_stop]>=dept_time, [dept_stop,arrvl_stop]].head(2)
    before=df.loc[df[dept_stop]<dept_time, [dept_stop,arrvl_stop]].tail(1)
    result=pd.concat([before,after])
    print(result)


#def query(day:str, dept_time:float, dept_stop:str, arrvl_stop:str):


def reverse_stops(stop_ids:str):
    reversed=stop_ids.split(", ")[::-1]
    for s in reversed:
        print(s,end=', ')

if __name__=="__main__":

    timetable=load_timetable("./raw_tables/seaford/seaford_to_adelaide__Sat_Sun_PH.txt")
    #timetable=pd.read_csv("./csv/seaford_to_adelaide_Mon_to_Fri.csv")

    search(timetable, 'Adelaide', 16.57, 'Hallett_Cove') 