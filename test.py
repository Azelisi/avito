# import json
# def add_json(id, content):
#     with open('db_dub.json', 'r', encoding='utf-8') as read_file:
#         data = json.load(read_file)
#         print(data)
#         if data.get(str(id)) == None: 
#             with open('db_dub.json', 'w', encoding='utf-8') as write_file:
#                 data_to_load = {
#                     str(id): [
#                         { 
#                         "content": content 
#                         }
#                     ]
#                     } 
#                 data.update(data_to_load)
#                 json.dump(data, fp=write_file, ensure_ascii=False, indent=2)
#         else:
#             with open('db_dub.json', 'w', encoding='utf-8') as write_file:
#                 data[str(id)].append({
#                     "content": content
#                 })
#                 json.dump(data, fp=write_file, ensure_ascii=False, indent=2)

# def read_json(id): 
#    with open('db_dub.json', 'r', encoding='utf-8') as read_file:
#        data = json.load(read_file)
#        if data.get(str(id)) == None:
#            return []
#        return data[str(id)]

# def clear_json(id): 
#     with open('db_dub.json', 'r', encoding='utf-8') as read_file:
#         data = json.load(read_file)
#         print(data)
#         if data.get(str(id)) != None: 
#             data[str(id)] = []
#             with open('db_dub.json', 'w', encoding='utf-8') as write_file:
#                 json.dump(data, fp=write_file, ensure_ascii=False, indent=2)

# print(read_json(32222)[1]['content'])
# element_id = 32222
# data = read_json(element_id)
# content = 'ass'
# if data and any(entry.get('content') == content for entry in data):
#     print(f"Элемент с ID {element_id} и содержанием '{content}' найден в файле JSON.")
# else:
#     print(f"Элемент с ID {element_id} и содержанием '{content}' не найден в файле JSON.")
data = {'<b></b>\n<b>тинкtinyurl.com/2b682dze</b>'}
print(data)