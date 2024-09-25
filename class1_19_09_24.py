class BinaryRelation:
    def __init__(self, element_pair: tuple, relation: int):
        self.x = element_pair[0]
        self.y = element_pair[1]
        self.element_pair = element_pair
        self.relation = relation

    def update_relation(self, new_relation: int) -> None:
        self.relation = new_relation


class MyFunction:
    def __init__(self, domain: set, codomain: set):
        self.domain = domain
        self.codomain = codomain
        self.cartesian = {(x, y) for x in self.domain for y in self.codomain}
        self.relations = {}  # Each relation is {(element_pair): BinaryRelation}

    def set_relations(self) -> None:
        self.relations = {}  # Clean all existing relations
        for element_pair in self.cartesian:
            relation = input(f'Enter relation for element pair {element_pair}: ')
            relation = int(relation)
            binary_relation = BinaryRelation(element_pair=element_pair, relation=relation)
            self.relations[element_pair] = binary_relation

    def update_relation(self, element_pair: tuple, new_relation) -> None:
        if not self.relations:
            raise ValueError('Set relations before updating single relation.')

        try:
            self.relations[element_pair].update_relation(new_relation)
        except KeyError:
            raise KeyError('Element pair non-existing in cartesian product.')

    def count_image_antecedent(self):
        """Count x's images and y's antecedents"""
        x_image_count = {}
        y_antecedent_count = {}
        for element_pair, binary_relation in self.relations.items():
            x, y = element_pair
            relation_value = binary_relation.relation
            if x in x_image_count:
                x_image_count[x] += relation_value
            else:
                x_image_count[x] = relation_value
            if y in y_antecedent_count:
                y_antecedent_count[y] += relation_value
            else:
                y_antecedent_count[y] = relation_value
        return x_image_count, y_antecedent_count

    def is_function(self) -> bool:
        x_image_count, _ = self.count_image_antecedent()
        for count in x_image_count.values():
            if count > 1:
                return False
        return True

    def is_application(self) -> bool:
        x_image_count, _ = self.count_image_antecedent()
        for count in x_image_count.values():
            if count != 1:
                return False
        return True

    def is_injective(self) -> bool:
        _, y_antecedent_count = self.count_image_antecedent()
        for count in y_antecedent_count.values():
            if count > 1:
                return False
        return True

    def is_surjective(self) -> bool:
        _, y_antecedent_count = self.count_image_antecedent()
        for y in self.codomain:
            if y_antecedent_count.get(y, 0) == 0:
                return False
        return True

    def is_bijective(self) -> bool:
        return self.is_injective() and self.is_surjective()
