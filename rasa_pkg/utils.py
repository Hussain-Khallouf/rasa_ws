import yaml


def read_yaml_file_content(path):
    with open(path, "r") as file:
        content = yaml.safe_load(file)
    return content


def write_yaml_content_to_file(path, content):
    with open(path, 'w') as file:
        yaml.dump(content, file)