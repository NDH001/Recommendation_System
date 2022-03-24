import pandas as pd
import random


def related(row):
    df = pd.read_csv('train_clean_manual.csv')
    row_index = row.index.to_list()
    df = df[~df.index.isin(row_index)]

    parameters = ['title', 'price', 'mileage', 'no_of_owners', 'type_of_vehicle', 'category', 'transmission']
    row = row[parameters]
    parts = df[parameters]

    title = row.title[0]
    type_of_vehicle = row.type_of_vehicle[0]
    categories = set(row.category[0].split(', '))
    price = row.price
    mileage = row.mileage
    owners = row.no_of_owners
    transmission = row.transmission

    def title_same(t):
        nonlocal title
        ori = set(title.split(' '))
        new = set(t.split(' '))
        return len(ori.intersection(new)) / len(ori)

    def type_same(t):
        nonlocal type_of_vehicle
        return 1 if t == type_of_vehicle else 0

    def category_similar(s):
        nonlocal categories
        s = set(s.split(', '))
        return len(categories.intersection(s))

    def price_abs(p):
        nonlocal price
        return abs(p - price)

    def mileage_abs(m):
        nonlocal mileage
        return abs(m - mileage)

    def owners_abs(o):
        nonlocal owners
        return abs(o - owners)

    def transmission_similar(t):
        nonlocal transmission
        return 1 if t == transmission else 0

    parts.title = parts['title'].apply(title_same)
    parts.type_of_vehicle = parts['type_of_vehicle'].apply(type_same)
    parts.category = parts['category'].apply(category_similar)
    parts.price = parts['price'].apply(price_abs)
    parts.mileage = parts['mileage'].apply(mileage_abs)
    parts.no_pf_owners = parts['no_of_owners'].apply(owners_abs)
    parts.transmission = parts['transmission'].apply(transmission_similar)

    parts = parts.sort_values(by=['title'], ascending=False)
    title_close = parts[:10]
    title_index = random.sample(title_close.index.to_list(), 5)
    parts = parts[~parts.index.isin(title_index)]

    m_type = parts.type_of_vehicle.max()
    m_category = parts.category.max()
    charac_same = parts[(parts.type_of_vehicle == m_type) & (parts.category == m_category)]
    charac_index = charac_same.index.to_list()
    if len(charac_index) >= 10: charac_index = random.sample(charac_index, 10)
    parts = parts[~parts.index.isin(charac_index)]

    parts = parts.sort_values(by=['price'], ascending=[True])
    price_close = parts[:20]
    price_index = random.sample(price_close.index.to_list(), 15)
    parts = parts[~parts.index.isin(price_index)]

    parts = parts.sort_values(by=['mileage'], ascending=[True])
    mileage_close = parts[:10]
    mileage_index = random.sample(mileage_close.index.to_list(), 5)
    parts = parts[~parts.index.isin(mileage_index)]

    parts = parts.sort_values(by=['no_of_owners'], ascending=[True])
    owners_close = parts[:10]
    owners_index = random.sample(owners_close.index.to_list(), 5)
    parts = parts[~parts.index.isin(owners_index)]

    transmission_same = parts[parts.transmission == 1]
    transmission_index = random.sample(transmission_same.index.to_list()[:10], 5)

    r_sample = random.sample(charac_index + price_index + mileage_index + owners_index + transmission_index, 5)
    ans = random.sample(r_sample + title_index, 10)[:5]
    return ans

