import json

with open("test.json") as file:
    input_data = json.load(file)
    print(len(input_data))

output_data = [v for v in {inp['link']: inp for inp in input_data}.values()]

print(len(output_data))

with open("data.json", 'w', encoding='utf-8') as file:
    json.dump(output_data, file, indent=4, ensure_ascii=False)
