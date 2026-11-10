
import math
import random
import numpy as np
import config

from simulation.organism import Organism
from simulation.genetics import inherit_traits


class Environment:
    def __init__(self):
        self.width = config.WORLD_WIDTH
        self.height = config.WORLD_HEIGHT

        self.food = []
        self.total_food_generated = 0
        self.regeneration_timer = 0.0

        self.organisms = []
        self.next_organism_id = 1

        self.elapsed_time = 0.0
        self.total_births = 0
        self.total_deaths = 0

        self.history = []
        self.history_timer = 0.0

        self.generate_initial_food()

        for _ in range(config.INITIAL_ORGANISM_COUNT):
            self.add_organism(
                Organism(self.next_organism_id)
            )
            self.next_organism_id += 1

    def add_organism(self, organism):
        if not hasattr(organism, "generation"):
            organism.generation = 0

        self.organisms.append(organism)

    def generate_initial_food(self):
        for _ in range(config.INITIAL_FOOD_COUNT):
            self.food.append((
                float(np.random.uniform(10, self.width - 10)),
                float(np.random.uniform(10, self.height - 10))
            ))

        self.total_food_generated += len(self.food)

    def regenerate_food(self):
        available = config.MAX_FOOD_COUNT - len(self.food)
        amount = min(
            available,
            config.FOOD_REGENERATION_AMOUNT
        )

        for _ in range(amount):
            self.food.append((
                float(np.random.uniform(10, self.width - 10)),
                float(np.random.uniform(10, self.height - 10))
            ))

        self.total_food_generated += amount

    def _nearest_food(self, organism):
        nearest_index = None
        nearest_distance = float("inf")

        vision = organism.vision

        for index, (fx, fy) in enumerate(self.food):
            distance = math.hypot(
                fx - organism.x,
                fy - organism.y
            )

            if distance <= vision and distance < nearest_distance:
                nearest_index = index
                nearest_distance = distance

        if nearest_index is None:
            return None, None

        return nearest_index, self.food[nearest_index]

    def _consume_food_if_close(self, organism):
        if not self.food:
            return

        eat_distance = config.FOOD_EAT_DISTANCE
        nearest_index = None
        nearest_distance = eat_distance

        for index, (fx, fy) in enumerate(self.food):
            distance = math.hypot(
                fx - organism.x,
                fy - organism.y
            )

            if distance <= nearest_distance:
                nearest_index = index
                nearest_distance = distance

        if nearest_index is not None:
            self.food.pop(nearest_index)
            organism.eat()

    def _reproduce(self, parent):
        living_count = len(self.living_organisms)

        if living_count >= config.MAX_POPULATION:
            return

        parent.reproduction_cost()
        traits = inherit_traits(parent)

        child = Organism(
            self.next_organism_id,
            x=parent.x + random.uniform(-8, 8),
            y=parent.y + random.uniform(-8, 8),
            traits=traits
        )

        child.generation = (
            getattr(parent, "generation", 0) + 1
        )

        child.energy = config.INITIAL_ENERGY * 0.65
        child.health = config.INITIAL_HEALTH

        self.next_organism_id += 1
        self.organisms.append(child)

        self.total_births += 1

    def update(self, delta_time):
        dt = max(
            0.0,
            min(float(delta_time), 0.25)
        )

        self.elapsed_time += dt

        for organism in list(self.organisms):
            if not organism.alive:
                continue

            target = None

            if organism.energy < config.FOOD_SEEK_ENERGY_THRESHOLD:
                _, target = self._nearest_food(organism)

            organism.move(dt, target)
            organism.update_needs(dt)

            self._consume_food_if_close(organism)

            if organism.can_reproduce():
                self._reproduce(organism)

        # Count each organism's death only once.
        for organism in self.organisms:
            if (
                not organism.alive
                and not getattr(organism, "_death_counted", False)
            ):
                self.total_deaths += 1
                organism._death_counted = True

        # Food regeneration.
        self.regeneration_timer += dt

        while self.regeneration_timer >= config.FOOD_REGEN_INTERVAL:
            self.regeneration_timer -= config.FOOD_REGEN_INTERVAL
            self.regenerate_food()

        # Record ecosystem observations once per second.
        self.history_timer += dt

        if self.history_timer >= 1.0:
            self.history_timer = 0.0

            living = self.living_organisms

            avg_energy = (
                sum(o.energy for o in living) / len(living)
                if living else 0.0
            )

            avg_size = (
                sum(o.size for o in living) / len(living)
                if living else 0.0
            )

            self.history.append({
                "time": round(self.elapsed_time, 2),
                "population": len(living),
                "food": len(self.food),
                "avg_energy": round(avg_energy, 2),
                "avg_size": round(avg_size, 3)
            })

            if len(self.history) > 3600:
                self.history.pop(0)

    @property
    def living_organisms(self):
        return [
            organism
            for organism in self.organisms
            if organism.alive
        ]

    def statistics(self):
        living = self.living_organisms

        avg_energy = (
            sum(o.energy for o in living) / len(living)
            if living else 0.0
        )

        avg_age = (
            sum(o.age for o in living) / len(living)
            if living else 0.0
        )

        avg_size = (
            sum(o.size for o in living) / len(living)
            if living else 0.0
        )

        highest_generation = max(
            (
                getattr(o, "generation", 0)
                for o in living
            ),
            default=0
        )

        return {
            "population": len(living),
            "food": len(self.food),
            "avg_energy": avg_energy,
            "avg_age": avg_age,
            "avg_size": avg_size,
            "births": self.total_births,
            "deaths": self.total_deaths,
            "generations": highest_generation,
            "largest_generation": highest_generation
        }
