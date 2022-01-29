import json
import random, string
import sys

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))


json_sample = {}
with open(sys.argv[1], "r") as read_file:
    json_sample = json.load(read_file)


def generate_random_type_with_value(exclude_type, keep_schema):
    if keep_schema:
        if exclude_type == 'str':
            negative_values = [random.randint(0,9999999), random.random(), bool(random.getrandbits(1)), None]
            return random.choice(negative_values)

        if exclude_type == 'int':
            negative_values = [randomword(25), random.random(), bool(random.getrandbits(1)), None]
            return random.choice(negative_values)

        if exclude_type == 'boolean':
            negative_values = [random.randint(0,9999999), random.random(), randomword(25), None]
            return random.choice(negative_values)

        if exclude_type == 'float':
            negative_values = [random.randint(0,9999999), randomword(25), bool(random.getrandbits(1)), None]
            return random.choice(negative_values)
        
        if exclude_type == None:
            negative_values = negative_values = [random.randint(0,9999999), randomword(25), bool(random.getrandbits(1))]
            return random.choice(negative_values)

def generate_fuzzed_json(one_random, keep_schema, sample):
    global data_type_of_value_has_been_changed
    local_keys = sample.keys()
    template_dict = {}
    if one_random == False & keep_schema:
        for i in local_keys:
            NoneType = type(None)
            if isinstance(sample[i], dict):
                template_dict[i] = generate_fuzzed_json(one_random, keep_schema, sample[i])

            if isinstance(sample[i], str):
                template_dict[i] = generate_random_type_with_value('str', keep_schema)

            if isinstance(sample[i], int):
                template_dict[i] = generate_random_type_with_value('int', keep_schema)

            if isinstance(sample[i], bool):
                template_dict[i] = generate_random_type_with_value('bool', keep_schema)

            if isinstance(sample[i], float):
                template_dict[i] = generate_random_type_with_value('float', keep_schema)

            if isinstance(sample[i], NoneType):
                template_dict[i] = generate_random_type_with_value(None, keep_schema)

            if isinstance(sample[i], list):
                element_list = []
                for el in sample[i]:
                    if isinstance(el, dict):
                        element_list.append(generate_fuzzed_json(one_random, keep_schema, el))
                    else:
                        element_listl.append('str')
                    template_dict[i] = element_list
        
    return template_dict

json_object = json.dumps(generate_fuzzed_json(False, True, json_sample))

sys.stdout.write(json_object)
sys.stdout.flush()
sys.exit(0)
