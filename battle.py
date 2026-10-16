from ex3 import FlameFactory, TransformCreatureFactory
from ex3.factory import CreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())


def test_battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    c1 = factory1.create_base()
    c2 = factory2.create_base()
    print(c1.describe())
    print("vs.")
    print(c2.describe())
    print("fight!")
    print(c1.attack())
    print(c2.attack())


def main() -> None:
    print("Testing factory")
    flame_factory = FlameFactory()
    test_factory(flame_factory)

    print("Testing factory")
    transform_factory = TransformCreatureFactory()
    test_factory(transform_factory)

    print("Testing battle")
    test_battle(flame_factory, transform_factory)

if __name__ == "__main__":
     main()
