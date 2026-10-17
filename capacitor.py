from ex3 import TransformCreatureFactory
from ex3.capability import TransformCapability


def main() -> None:
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()

    base = factory.create_base()
    evolved = factory.create_evolved()

    print("base:")
    print(base.describe())
    print(base.attack())
    if isinstance(base, TransformCapability):
        print(base.transform())
        print(base.attack())
        print(base.revert())

    print("evolved:")
    print(evolved.describe())
    print(evolved.attack())
    if isinstance(evolved, TransformCapability):
        print(evolved.transform())
        print(evolved.attack())
        print(evolved.revert())

    print(
        "\nA capability is an abstract class "
        "deliberately not a Creature."
    )
    print(
        "What would break, or become impossible, if you had put "
        "transform and revert on the Creature base class instead?"
    )
    print(
        "If transform and revert were part of the Creature base class, "
        "every entity in the game would be forced to implement or handle "
        "transform/revert behavior, violating the Interface Segregation "
        "Principle."
    )


if __name__ == "__main__":
    main()
