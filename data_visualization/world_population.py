# -*- coding:utf-8 -*-

import json
from pygal_maps_world.i18n import COUNTRIES
import pygal
from pygal.style import RotateStyle


def get_country_code(country_name):
    """根据国家名字返回对应code"""
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    return None


filename = "population_data.json"
with open(filename) as f:
    pop_data = json.load(f)

cc_population = {}
for pop_dict in pop_data:
    if pop_dict['Year'] == '2010':
        country_name = pop_dict['Country Name']
        population = int(float(pop_dict['Value']))
        code = get_country_code(country_name)
        if code:
            cc_population[code] = population

# 按人口数量进行分组
cc_pop_high, cc_pop_mid, cc_pop_low = {}, {}, {}
for cc, pop in cc_population.items():
    if pop < 10000000:
        cc_pop_low[cc] = pop
    elif pop < 1000000000:
        cc_pop_mid[cc] = pop
    else:
        cc_pop_high[cc] = pop

print(len(cc_pop_low), len(cc_pop_mid), len(cc_pop_high))

wm_all = pygal.maps.world.World()
wm_all.title = "World Population in 2010, by coutry"
wm_all.add('0-10m', cc_pop_low)
wm_all.add('10m-1bn', cc_pop_mid)
wm_all.add('>1bn', cc_pop_high)

wm_all.render_to_file("world_population_2010.svg")