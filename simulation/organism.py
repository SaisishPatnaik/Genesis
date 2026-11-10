
import math
import random
import config


class Organism:
    def __init__(self, organism_id, x=None, y=None, traits=None):
        self.id = organism_id
        self.x = random.uniform(10, config.WORLD_WIDTH - 7) if x is None else float(x)
        self.y = random.uniform(10, config.WORLD_HEIGHT - 7) if y is None else float(y)

        traits = traits or {}
        self.speed = float(traits.get("speed", random.uniform(1.0, 3.0)))
        self.vision = float(traits.get("vision", random.uniform(40.0, 100.0)))
        self.metabolism = float(traits.get("metabolism", random.uniform(0.5, 1.5)))

        # Physical growth
        self.size = float(traits.get("size", 1.0))
        self.min_size = 0.7
        self.max_size = 1.8
        self.growth_rate = 0.006
        self.growth_energy_threshold = config.MAX_ENERGY * 0.70
        self.growth_energy_cost = 0.5

        self.energy = config.INITIAL_ENERGY
        self.health = config.INITIAL_HEALTH
        self.age = 0.0
        self.alive = True

        angle = random.uniform(0, math.tau)
        self.direction_x = math.cos(angle)
        self.direction_y = math.sin(angle)
        self.direction_timer = 0.0
        self.direction_change_interval = random.uniform(
            config.WANDER_TURN_MIN, config.WANDER_TURN_MAX
        )
        self.reproduction_cooldown = random.uniform(0.0, 3.0)
        self.state = "WANDERING"

    def _choose_direction(self):
        angle = random.uniform(0, math.tau)
        self.direction_x = math.cos(angle)
        self.direction_y = math.sin(angle)
        self.direction_timer = 0.0
        self.direction_change_interval = random.uniform(
            config.WANDER_TURN_MIN, config.WANDER_TURN_MAX
        )

    def move(self, dt, target=None):
        if not self.alive:
            return

        if target is not None:
            dx, dy = target[0] - self.x, target[1] - self.y
            distance = math.hypot(dx, dy)
            if distance > 0:
                self.direction_x, self.direction_y = dx / distance, dy / distance
            self.state = "SEEKING FOOD"
        else:
            self.state = "WANDERING"
            self.direction_timer += dt
            if self.direction_timer >= self.direction_change_interval:
                self._choose_direction()

        magnitude = math.hypot(self.direction_x, self.direction_y)
        if magnitude:
            self.x += (self.direction_x / magnitude) * self.speed * config.MOVEMENT_SCALE * dt
            self.y += (self.direction_y / magnitude) * self.speed * config.MOVEMENT_SCALE * dt

        radius = 10
        if self.x < radius or self.x > config.WORLD_WIDTH - radius:
            self.direction_x *= -1
        if self.y < radius or self.y > config.WORLD_HEIGHT - radius:
            self.direction_y *= -1
        self.x = max(radius, min(self.x, config.WORLD_WIDTH - radius))
        self.y = max(radius, min(self.y, config.WORLD_HEIGHT - radius))

    def update_needs(self, dt):
        if not self.alive:
            return

        self.age += dt
        self.reproduction_cooldown = max(0.0, self.reproduction_cooldown - dt)
        self.energy -= config.BASE_ENERGY_CONSUMPTION * self.metabolism * dt
        self.energy = max(0.0, self.energy)

        # Update physical growth
        self.update_growth(dt)

        if self.energy <= 0:
            self.health -= config.STARVATION_DAMAGE_PER_SECOND * dt
            if self.health <= 0:
                self.health = 0
                self.alive = False

    def update_growth(self, dt):
        if not self.alive:
            return

        if (
            self.energy >= self.growth_energy_threshold
            and self.size < self.max_size
        ):
            self.size = min(
                self.max_size,
                self.size + self.growth_rate * dt
            )

            self.energy = max(
                0.0,
                self.energy - self.growth_energy_cost * dt
            )

    def eat(self):
        if self.alive:
            self.energy = min(config.MAX_ENERGY, self.energy + config.FOOD_ENERGY)

    def can_reproduce(self):
        return (
            self.alive
            and self.energy >= config.REPRODUCTION_ENERGY
            and self.reproduction_cooldown <= 0
        )

    def reproduction_cost(self):
        self.energy = max(0.0, self.energy - config.REPRODUCTION_COST)
        self.reproduction_cooldown = config.REPRODUCTION_COOLDOWN
