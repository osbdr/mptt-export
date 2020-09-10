from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

import json
import toml
import yaml


class Entry(MPTTModel):
    content = models.CharField(max_length=500)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.content

    def to_dict(self):
        children = self.get_children()
        if all(child.is_leaf_node() for child in children):
            a = [child.content for child in children]
            if len(a) > 1:
                return a
            return a[0]
        elif all(not child.is_leaf_node() for child in children):
            keys = [child.content for child in children]
            values = [child.to_dict() for child in children]
            return dict(zip(keys, values))
        else:
            raise ValueError("Invalid Structure: Mixed K/V and Arrays")
 
    def to_json(self):
        return json.dumps(self.to_dict())

    def to_toml(self):
        return toml.dumps(self.to_dict())

    def to_yaml(self):
        return yaml.dump(self.to_dict())

    def to_nginx(self):
        children = self.get_children()
        if len(children) > 0:
            return "".join([child.nginx_helper() for child in children])
        return ""

    def nginx_helper(self):
        indent = "\t" * (self.level - 1)
        if self.is_leaf_node():
            return f'{indent}{self.content};\n'

        children = self.get_children()
        if all(child.is_leaf_node() for child in children):
            child_entries = " ".join([child.content for child in children])
            return f'{indent}{self.content} {child_entries};\n'
        else:
            child_entries = "".join([child.nginx_helper() for child in children])
            return f'{indent}{self.content} {{\n{child_entries}{indent}}}\n'
