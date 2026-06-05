"""Exportação de tabelas e gráficos dos benchmarks.

Este módulo usa apenas biblioteca padrão para que a execução pelo terminal seja
possível mesmo antes da instalação das dependências da interface Streamlit.
"""

from __future__ import annotations

import csv
from pathlib import Path


def save_results(summary: list[dict[str, float | int | str]], output_dir: Path) -> tuple[Path, Path, Path]:
    """Salva tabela CSV e gráficos SVG para tempo e memória."""

    output_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_dir / "resultados_resumo.csv"
    time_plot_path = output_dir / "grafico_tempo.svg"
    memory_plot_path = output_dir / "grafico_memoria.svg"

    _save_csv(summary, csv_path)
    _save_svg_line_chart(
        summary,
        y_column="avg_time_seconds",
        y_label="Tempo médio (s)",
        title="Tempo médio por tamanho de grafo",
        output_path=time_plot_path,
    )
    _save_svg_line_chart(
        summary,
        y_column="avg_peak_memory_kb",
        y_label="Pico médio de memória (KB)",
        title="Memória aproximada por tamanho de grafo",
        output_path=memory_plot_path,
    )

    return csv_path, time_plot_path, memory_plot_path


def _save_csv(summary: list[dict[str, float | int | str]], output_path: Path) -> None:
    if not summary:
        output_path.write_text("", encoding="utf-8")
        return

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(summary[0].keys()))
        writer.writeheader()
        writer.writerows(summary)


def _save_svg_line_chart(
    summary: list[dict[str, float | int | str]],
    y_column: str,
    y_label: str,
    title: str,
    output_path: Path,
) -> None:
    width, height = 920, 520
    left, right, top, bottom = 90, 28, 54, 72
    plot_width = width - left - right
    plot_height = height - top - bottom

    if not summary:
        output_path.write_text("<svg xmlns='http://www.w3.org/2000/svg'></svg>", encoding="utf-8")
        return

    vertices_values = sorted({int(item["vertices"]) for item in summary})
    y_values = [float(item[y_column]) for item in summary]
    min_x, max_x = min(vertices_values), max(vertices_values)
    min_y, max_y = 0.0, max(y_values) if y_values else 1.0
    if max_y == 0:
        max_y = 1.0
    if min_x == max_x:
        max_x = min_x + 1

    def x_scale(value: int) -> float:
        return left + ((value - min_x) / (max_x - min_x)) * plot_width

    def y_scale(value: float) -> float:
        return top + plot_height - ((value - min_y) / (max_y - min_y)) * plot_height

    palette = {
        "Dijkstra (todas as origens)": "#2563eb",
        "Floyd-Warshall": "#dc2626",
    }
    grouped: dict[str, list[dict[str, float | int | str]]] = {}
    for item in summary:
        grouped.setdefault(str(item["algorithm"]), []).append(item)

    svg: list[str] = [
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>",
        "<rect width='100%' height='100%' fill='#ffffff'/>",
        f"<text x='{width / 2}' y='28' text-anchor='middle' font-family='Arial' font-size='20' font-weight='700' fill='#172033'>{title}</text>",
        f"<line x1='{left}' y1='{top + plot_height}' x2='{left + plot_width}' y2='{top + plot_height}' stroke='#334155'/>",
        f"<line x1='{left}' y1='{top}' x2='{left}' y2='{top + plot_height}' stroke='#334155'/>",
    ]

    for tick in range(6):
        y_value = min_y + (max_y - min_y) * tick / 5
        y = y_scale(y_value)
        svg.append(f"<line x1='{left}' y1='{y:.2f}' x2='{left + plot_width}' y2='{y:.2f}' stroke='#e2e8f0'/>")
        svg.append(
            f"<text x='{left - 10}' y='{y + 4:.2f}' text-anchor='end' font-family='Arial' font-size='12' fill='#475569'>{y_value:.4f}</text>"
        )

    for vertex in vertices_values:
        x = x_scale(vertex)
        svg.append(f"<line x1='{x:.2f}' y1='{top + plot_height}' x2='{x:.2f}' y2='{top + plot_height + 5}' stroke='#334155'/>")
        svg.append(
            f"<text x='{x:.2f}' y='{top + plot_height + 24}' text-anchor='middle' font-family='Arial' font-size='12' fill='#475569'>{vertex}</text>"
        )

    for index, (algorithm, items) in enumerate(grouped.items()):
        items = sorted(items, key=lambda item: int(item["vertices"]))
        color = palette.get(algorithm, "#0f766e")
        points = " ".join(
            f"{x_scale(int(item['vertices'])):.2f},{y_scale(float(item[y_column])):.2f}" for item in items
        )
        svg.append(f"<polyline fill='none' stroke='{color}' stroke-width='3' points='{points}'/>")
        for item in items:
            x = x_scale(int(item["vertices"]))
            y = y_scale(float(item[y_column]))
            svg.append(f"<circle cx='{x:.2f}' cy='{y:.2f}' r='4' fill='{color}'/>")

        legend_x = left + 16
        legend_y = top + 22 + index * 24
        svg.append(f"<rect x='{legend_x}' y='{legend_y - 10}' width='14' height='14' fill='{color}' rx='2'/>")
        svg.append(
            f"<text x='{legend_x + 22}' y='{legend_y + 2}' font-family='Arial' font-size='13' fill='#172033'>{algorithm}</text>"
        )

    svg.append(
        f"<text x='{left + plot_width / 2}' y='{height - 24}' text-anchor='middle' font-family='Arial' font-size='14' fill='#172033'>Número de vértices</text>"
    )
    svg.append(
        f"<text x='24' y='{top + plot_height / 2}' text-anchor='middle' font-family='Arial' font-size='14' fill='#172033' transform='rotate(-90 24 {top + plot_height / 2})'>{y_label}</text>"
    )
    svg.append("</svg>")

    output_path.write_text("\n".join(svg), encoding="utf-8")
