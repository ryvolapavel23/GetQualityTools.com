"""
Pareto Chart Generator (80/20 Rule) for Quality Engineers.
Standalone script for automotive root-cause analysis and defect prioritization.

Part of the open quality tools initiative:
- Global (EN): https://getqualitytools.com
- Czech (CS):  https://nastrojekvality.cz
- Polish (PL): https://narzedziajakosci.pl
"""

import matplotlib.pyplot as plt
from typing import Dict, Optional


def generate_pareto_chart(
    data: Dict[str, int],
    threshold: int = 80,
    limit: int = 10,
    output_file: Optional[str] = "pareto_chart.png"
) -> None:
    """
    Generates a dual-axis Pareto Chart combining defect frequencies
    with a cumulative percentage line curve.
    """
    # 1. Sort defects descending and apply limit
    sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)[:limit]
    categories = [item[0] for item in sorted_data]
    counts = [item[1] for item in sorted_data]
    total_count = sum(counts)

    if total_count == 0:
        raise ValueError("Total defects count cannot be zero.")

    # 2. Calculate cumulative percentage
    cumulative_pct = [
        (sum(counts[: i + 1]) / total_count) * 100 for i in range(len(counts))
    ]

    # 3. Render chart
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Bar chart for absolute defect counts
    bars = ax1.bar(categories, counts, color="#0d6efd", width=0.6)
    ax1.set_ylabel("Defect Count", color="#0d6efd", fontweight="bold")
    ax1.tick_params(axis="y", labelcolor="#0d6efd")
    ax1.bar_label(bars, padding=3, color="#0d6efd", fontweight="bold")
    plt.xticks(rotation=30, ha="right")

    # Secondary axis for cumulative percentage curve
    ax2 = ax1.twinx()
    ax2.plot(categories, cumulative_pct, color="#dc3545", marker="D", ms=6, linewidth=2)
    ax2.set_ylabel("Cumulative Share (%)", color="#dc3545", fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="#dc3545")
    ax2.set_ylim(0, 115)

    # Reference 80/20 threshold line
    ax2.axhline(threshold, color="#f59e0b", linestyle="--", linewidth=1.5)
    ax2.text(
        len(categories) - 1,
        threshold + 2,
        f"Pareto Cut-off ({threshold}%)",
        color="#f59e0b",
        ha="right",
        fontweight="bold",
    )

    plt.title("Automotive Defect Pareto Analysis (80/20 Principle)", pad=15, fontweight="bold")
    fig.tight_layout()

    if output_file:
        plt.savefig(output_file, dpi=300)
        print(f"Pareto chart successfully saved to: {output_file}")
    else:
        plt.show()

    plt.close(fig)


if __name__ == "__main__":
    # Real-world automotive sample data (e.g. injection moulding defects)
    defect_sample = {
        "Scratches / Povrchové škrábance": 420,
        "Short shot / Nedostříknutí dílu": 260,
        "Flash / Otřepy na dělicí rovině": 140,
        "Sink marks / Propadliny": 45,
        "Silver streaks / Stříbření": 30,
        "Weld lines / Studené spoje": 20,
        "Color mismatch / Odstín barvy": 15,
        "Deformation / Zkroucení dílu": 10,
    }

    generate_pareto_chart(defect_sample, threshold=80, output_file="pareto_chart.png")
