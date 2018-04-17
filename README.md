# wrs
This module is designed for Human Navigation in virtual space.
This module is composed of functions allowing to generate a sentence to
describe the position of a target object.
#required json structure:

message (task_info)

environment (map layout)

furniture (furniture layout)

#dictionaries:

furniture

object

relation

launch: python3 nlg.py

#expected output:

object: bottle

room name: kitchen

piece of furniture: table

relation: on top of

Go to the kitchen

Find the table

Take the bottle on top of the table


pylint score: 9.05

