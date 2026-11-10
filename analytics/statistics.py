import csv
from pathlib import Path
from simulation.genetics import genetic_diversity


def export_history(environment, filepath="data/genesis_history.csv"):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    fields = ["time", "population", "food", "avg_energy"]
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(environment.history)
    return path


def research_snapshot(environment):
    living = environment.living_organisms
    stats = environment.statistics()
    stats["genetic_diversity"] = genetic_diversity(living)
    stats["total_food_generated"] = environment.total_food_generated
    stats["elapsed_time"] = environment.elapsed_time
    return stats
