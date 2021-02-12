import pandas as pd
import os 
from tqdm import tqdm
import json
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from datetime import datetime

mobility_data_location = '/home/arrow/safegraph'


cbgs = {
    'newyorkcity': ['36047', '36081', '36061', '36005', '36085', '36119', '34003', '34017', '34031', '36079', '36087'],
    'boston': ['25021', '25023', '25025', '25009', '25017', '33015', '33017'],
    'seattle': ['53033', '53061', '53053', '53035', '53067', '53057', '53029', '53045'],
    'miami': ['12086', '12011', '12099'],
    'chicago': ['17031', '17037', '17043', '17063', '17091', '17089', '17093', '17111', '17197'],
    'dallas': ['48085', '48113', '48121', '48139', '48231', '48257', '48397', '48251', '48367', '48439', '48497'],
}



# newyorkcity = ['36047', '36081', '36061', '36005', '36085', '36119', '34003', '34017', '34031', '36079', '36087']
# boston = ['25021']
# seattle = ['53033', '53061', '53053']
# miami = []
# chicago = []
# dallas = []

# df = pd.read_csv('/home/arrow/safegraph/2019/01/01/2019-01-01-social-distancing.csv.gz', compression='gzip', header=0,  quotechar='"', error_bad_lines=False)
# print(df.iloc[1])
# # print(df.shape[0])
# for i in range(df.shape[0]):
#     # print(i)
#     src = str(df.iloc[i].origin_census_block_group)
#     if len(src) < 12:
#         src = '0' + src
#     # print(src)
#     dst_cbgs = json.loads(df.iloc[i].destination_cbgs)
#     if src in dst_cbgs:
#         # print(src)
#         pass
#     else:
#         print('error')
# if df.iloc[1].origin_census_block_group in dst_cbgs:
#     print(df.iloc[1].origin_census_block_group)


def process_mobility(years, months):
    for city in cbgs:
        locals()[city+'_mobility'] = []
        locals()[city+'_today'] = 0
        locals()[city+'_cbg_num'] = 0
    
    datex = []

    for yr in years:
        year_dir = os.path.join(mobility_data_location, yr)
        print(year_dir)
        # for mth in tqdm(os.listdir(year_dir)):
        for mth in tqdm(months):
            month_dir = os.path.join(year_dir, mth)
            print(month_dir)
            for d in tqdm(os.listdir(month_dir)):
            # for d in tqdm(['01', '02']):
                datevalue = yr + '-' + mth + '-' + d
                if datevalue not in datex:
                    datex.append(datevalue)

                day_dir = os.path.join(month_dir, d)
                # print(day_dir)
                filename = datevalue + '-social-distancing.csv.gz'
                day_file = os.path.join(day_dir, filename)
                # print(day_file)

                df = pd.read_csv(day_file, compression='gzip', header=0,  quotechar='"', error_bad_lines=False)
                for city in cbgs:
                    locals()[city+'_today'] = 0
                    locals()[city+'_cbg_num'] = 0

                for i in tqdm(range(df.shape[0])):
                    src = str(df.iloc[i].origin_census_block_group)
                    # print(len(src))
                    if len(src) < 12:
                        src = '0' + src
                        # print(src[0:5])
                    for city in cbgs:
                        # print(src[0:5], cbgs[city])
                        if src[0:5] in cbgs[city]:
                            # print(df.iloc[i].device_count - df.iloc[i].completely_home_device_count)
                            # print(df.iloc[i].device_count, df.iloc[i].completely_home_device_count)
                            locals()[city+'_today'] += float(df.iloc[i].device_count - df.iloc[i].completely_home_device_count)/df.iloc[i].device_count
                            locals()[city+'_cbg_num'] += 1
                            break
                
                for city in cbgs:
                    if locals()[city+'_today'] > 0:
                        locals()[city+'_mobility'].append(float(locals()[city+'_today'] / locals()[city+'_cbg_num']))
                    else:
                        locals()[city+'_mobility'].append(float(locals()[city+'_today']))

    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")

    for city in cbgs:
        plt.figure()
        print(datex, locals()[city+'_mobility'])
        plt.plot(datex, locals()[city+'_mobility'], label=city, marker='.')
        plot_location = mobility_data_location + '/mobilityplot/' + city + years[0] + months[0] + '.png'
        plt.legend(loc='best')
        plt.show()
        plt.savefig(plot_location)  

        csv_location = mobility_data_location + '/mobilityplot/' + city + years[0] + months[0] + '.csv'
        mobility = {'0_date':datex, city:locals()[city+'_mobility']}
        print(mobility)
        df = pd.DataFrame.from_dict(mobility)
        df.to_csv(csv_location, index=False)     

years = ['2019']
months = ['01']

process_mobility(years, months)