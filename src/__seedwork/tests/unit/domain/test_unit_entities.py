import unittest
from abc import ABC
from dataclasses import dataclass, is_dataclass
from __seedwork.domain.entities import Entity

from __seedwork.domain.value_objects import UniqueEntityId


@dataclass(frozen=True, kw_only=True)
class StubEntity(Entity):
    prop1: str
    prop2: str


class TestEntityUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Entity))

    def test_if_is_a_abstract_class(self):
        self.assertIsInstance(Entity(), ABC)

    def test_set_id_and_props(self):
        entity = StubEntity(prop1="value1", prop2="value2")
        self.assertEqual(entity.prop1, "value1")
        self.assertEqual(entity.prop2, "value2")
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)
        self.assertEqual(entity.unique_entity_id.id, entity.id)

    def test_accept_a_valid_uuid(self):
        entity = StubEntity(unique_entity_id=UniqueEntityId("9f2ec4aa-010b-4282-addb-6d738cc27676"),
                            prop1="value1",
                            prop2="value2")

        self.assertEqual(entity.id, "9f2ec4aa-010b-4282-addb-6d738cc27676")

    def test_to_dict_method(self):
        entity = StubEntity(unique_entity_id=UniqueEntityId("9f2ec4aa-010b-4282-addb-6d738cc27676"),
                            prop1="value1",
                            prop2="value2")

        self.assertDictEqual(entity.to_dict(), {
            "id": "9f2ec4aa-010b-4282-addb-6d738cc27676",
            "prop1": "value1",
            "prop2": "value2"
        })

    # pylint: disable=protected-access
    def test_set_attributes(self):
        entity = StubEntity(prop1="val1", prop2="val2")
        entity._set("prop1", "new_val")
        self.assertEqual(entity.prop1, "new_val")
