import json
from catalog.models import Brand 

# with open('data/brands_models.json', 'r') as file:
#     brands = json.load(file)

# for brand_name in brands:
#     Brand.objects.get_or_create(name=brand_name)
#     print(brand_name + ' creado')
    
def load_data_json(json_name, model):
    with open(f'data/{json_name}.json', 'r') as file:
        data = json.load(file)
    
    for item in data:
        model.objects.get_or_create(name=item)
        print(item + ' creado')

