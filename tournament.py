from ex3 import FlameFactory, TransformCreatureFactory
from ex3.factory import CreatureFactory
from ex4 import (
    AggressiveStrategy,
    BattleStrategy,
    InvalidCreatureError,
    NormalStrategy,
)


def run_tournament(
    name: str,
    opponents: list[tuple[CreatureFactory, BattleStrategy]],
) -> None:
    print(name)
    pairs_desc = []
    for factory, strategy in opponents:
        c = factory.create_base()
        strat_name = strategy.__class__.__name__.replace("Strategy", "")
        pairs_desc.append(f"({c.name}+{strat_name})")
    print(f"[ {', '.join(pairs_desc)} ]")
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    print("- Battle *")

    try:
        for i in range(len(opponents)):
            for j in range(i + 1, len(opponents)):
                fac1, strat1 = opponents[i]
                fac2, strat2 = opponents[j]
                c1 = fac1.create_base()
                c2 = fac2.create_base()

                print(c1.describe())
                print("vs.")
                print(c2.describe())
                print("now fight!")

                if not strat1.is_valid(c1):
                    strat1.act(c1)
                else:
                    strat1.act(c1)
                    strat2.act(c2)
        print()
    except InvalidCreatureError as e:
        print(f"Battle error, aborting tournament: {e}")


def main() -> None:
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()

    normal_strat = NormalStrategy()
    aggressive_strat = AggressiveStrategy()

    run_tournament(
        "Tournament 0 (basic)",
        [
            (flame_factory, normal_strat),
            (transform_factory, aggressive_strat),
        ],
    )

    run_tournament(
        "Tournament 1 (error)",
        [
            (transform_factory, aggressive_strat),
            (flame_factory, aggressive_strat),
        ],
    )

    print(
        "\nThe tournament code never checks which family an entity "
        "belongs to, yet each one fights differently. Where did that "
        "decision move to, and what does that buy you the day a "
        "new capability is added?"
    )
    print(
        "The decision moved into the strategy classes (via isinstance "
        "capability checks). When adding a new capability, you simply "
        "add a new strategy class without altering tournament "
        "execution logic."
    )


if __name__ == "__main__":
    main()
