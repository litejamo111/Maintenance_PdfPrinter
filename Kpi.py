import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter
import datetime

def plot_week_kpis(start_date, end_date, daily_data):
    dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    
    def aggregate_daily_data(daily_data):
        satisfaction = []
        response_times = []
        total_issues = 0
        
        for date, issues in daily_data.items():
            if issues:
                avg_satisfaction = np.mean([issue['satisfaction'] for issue in issues])
                avg_response_time = np.mean([issue['response_time'] for issue in issues])
                satisfaction.append(avg_satisfaction)
                response_times.append(avg_response_time)
                total_issues += len(issues)
            else:
                satisfaction.append(np.nan)
                response_times.append(np.nan)
        
        return satisfaction, response_times, total_issues

    def plot_month(ax, dates, satisfaction, response_times, total_issues):
        # Satisfaction plot
        color1 = '#1f77b4'  # A vibrant blue
        ax.set_xlabel('Fecha de Incidente', fontsize=12)
        ax.set_ylabel('Tasa de Satisfacción', color=color1, fontsize=12)
        ax.plot(dates, satisfaction, color=color1, marker='o', linewidth=2, markersize=6, label='Tasa de Satisfacción')
        ax.tick_params(axis='y', labelcolor=color1, labelsize=10)
        ax.set_ylim(1, 5)
        avg_satisfaction = np.nanmean(satisfaction)
        ax.axhline(avg_satisfaction, color=color1, linestyle='--', linewidth=2,
                   label=f'Promedio Satisfacción: {avg_satisfaction:.2f}')
        
        # Response time plot
        ax2 = ax.twinx()
        color2 = '#2ca02c'  # A vibrant green
        ax2.set_ylabel('Tiempo de Respuesta (minutos)', color=color2, fontsize=12)
        ax2.plot(dates, response_times, color=color2, marker='s', linewidth=2, markersize=6,
                 linestyle='--', label='Tiempo de Respuesta')
        ax2.tick_params(axis='y', labelcolor=color2, labelsize=10)
        avg_response = np.nanmean(response_times)
        ax2.axhline(avg_response, color=color2, linestyle=':', linewidth=2,
                    label=f'Promedio Respuesta: {avg_response:.2f} min')
        
        # Title and x-axis formatting
        ax.set_title(f'KPIs de TI - {dates[0].strftime("%d %b")} al {dates[-1].strftime("%d %b %Y")}', fontsize=14, fontweight='bold')
        ax.xaxis.set_major_formatter(DateFormatter('%d-%m'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
        
        # Legend
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10, framealpha=0.7)
        
        # Grid
        ax.grid(True, linestyle=':', alpha=0.6)
        
        # Add fixed label on the top right corner
        plt.text(1, 1.05, f'{total_issues} de 6 Novedades resueltas', transform=ax.transAxes, fontsize=12, fontweight='bold',
                 verticalalignment='top', horizontalalignment='right', bbox=dict(facecolor='white', alpha=0.8))

    # Aggregate daily data
    satisfaction, response_times, total_issues = aggregate_daily_data(daily_data)

    # Plotting
    try:
        plt.style.use('ggplot')
    except:
        print("ggplot style not available, using default style")
    
    fig, ax = plt.subplots(figsize=(14, 10))
    plot_month(ax, dates, satisfaction, response_times, total_issues)
    plt.tight_layout()
    plt.show()

# Example usage:
start_date = datetime.datetime(2024, 8, 19)
end_date = datetime.datetime(2024, 8, 23)

daily_data = {
    datetime.datetime(2024, 8, 19): [
        {'satisfaction': 3.9, 'response_time': 47}
    ],
    datetime.datetime(2024, 8, 20): [
        {'satisfaction': 4.0, 'response_time': 55}
    ],
    datetime.datetime(2024, 8, 21): [
        {'satisfaction': 4.2, 'response_time': 49},
        
    ],
    datetime.datetime(2024, 8, 22): [
        {'satisfaction': 4.8, 'response_time': 60}
    ],
    datetime.datetime(2024, 8, 23): [
        {'satisfaction': 4.5, 'response_time': 41},
        {'satisfaction': 3.9, 'response_time': 47}
    ]
}

plot_week_kpis(start_date, end_date, daily_data)