
import random
import config


TRAIT_NAMES = ("speed", "vision", "metabolism", "size")


def inherit_traits(parent):
    """Inherit parental traits with small bounded mutations."""

    child_traits = {}

    for name in TRAIT_NAMES:
        value = getattr(parent, name)

        if random.random() < config.MUTATION_RATE:
            value *= random.uniform(
                1.0 - config.MUTATION_STRENGTH,
                1.0 + config.MUTATION_STRENGTH
            )

        child_traits[name] = value

    # Keep inherited traits within reasonable limits
    child_traits["speed"] = max(0.5, min(4.0, child_traits["speed"]))
    child_traits["vision"] = max(20.0, min(150.0, child_traits["vision"]))
    child_traits["metabolism"] = max(0.3, min(2.0, child_traits["metabolism"]))
    child_traits["size"] = max(0.7, min(1.8, child_traits["size"]))

    return child_traits


def genetic_diversity(organisms):
    """Calculate average coefficient of variation across inherited traits."""

    living = [o for o in organisms if o.alive]

    if len(living) < 2:
        return 0.0

    cvs = []

    for name in TRAIT_NAMES:
        values = [getattr(o, name) for o in living]

        mean = sum(values) / len(values)

        if mean:
            variance = sum((v - mean) ** 2 for v in values) / len(values)
            cvs.append((variance ** 0.5) / mean)

    return sum(cvs) / len(cvs) if cvs else 0.0
