#Li Yury 22102550
import sys
def normalize_data(n_cases, n_people, scale):
    # TODO) Calculate the number of cases per its population
    norm_cases = [round((cases / population) * scale, 2) for cases, population in zip(n_cases, n_people)]
    return norm_cases
regions  = ['Seoul', 'Gyeongi', 'Busan', 'Gyeongnam', 'Incheon', 'Gyeongbuk', 'Daegu', 'Chungnam', 'Jeonnam', 'Jeonbuk', 'Chungbuk', 'Gangwon', 'Daejeon', 'Gwangju', 'Ulsan', 'Jeju', 'Sejong']
n_people = [9550227,  13530519, 3359527,     3322373,   2938429,     2630254, 2393626,    2118183,   1838353,   1792476,    1597179,   1536270,   1454679,   1441970, 1124459, 675883,   365309] # 2021-08
n_covid  = [    644,       529,      38,          29,       148,          28,      41,         62,        23,        27,         27,        33,        16,        40,      20,      5,        4] # 2021-09-21

sum_people = 0  
for num in n_people:
    sum_people+=num
sum_covid  = 0
for num in n_covid:
    sum_covid+=num
norm_covid = normalize_data(n_covid, n_people, 1000000)

# Print population by region
markdown_table = '## Korean Population by Region\n'
markdown_table += '* Total population: {}\n\n'.format(sum_people)
markdown_table += '| Region | Population | Ratio (%) |\n'
markdown_table += '| ------ | ---------- | --------- |\n'
for idx, pop in enumerate(n_people):
    ratio = (n_people[idx] / sum_people) * 100 
    markdown_table += '| {} | {} | {:.1f} |\n'.format(regions[idx], pop, ratio)
print(sum_covid)


markdown_table += '\n## COVID-19 New Cases by Region (per 1 million people)\n'
markdown_table += '* Total new cases: {}\n\n'.format(sum_covid)
markdown_table += '| Region | New Cases (per 1M) | Ratio (%) | Amount of New Cases |\n'
markdown_table += '| ------ | ------------------ | --------- | --------------------- |\n'
for idx, cases in enumerate(norm_covid):
    ratio = (n_covid[idx] / sum_covid) * 100
    markdown_table += '| {} | {} | {:.1f} | {:.1f} |\n'.format(regions[idx], n_covid[idx], ratio, cases)
with open ("covid19_statistics.md","w") as f:
    f.write(markdown_table)
sys.stdout = sys.__stdout__
print("Tables have been written to covid19_statistics.md")