#  модели данных для Neo4j с использованием neomodel

from neomodel import StructuredNode, StringProperty, RelationshipTo

class Person(StructuredNode):
    name = StringProperty(unique_index=True)
    age = StringProperty()
    friends = RelationshipTo('Person', 'FRIENDS_WITH')
