import matplotlib.pyplot as plt
import numpy as np

# Data
total_pcs = 74
active_pcs = 58
free_pcs = total_pcs - active_pcs
first_week_progress = 13
second_week_progress = 33
third_week_progress = 54
forth_week_progress = 74

# Plotting
fig, ax = plt.subplots(figsize=(14, 6))

# Colors
first_week_color = '#1f77b4'  # Blue for first week
second_week_color = '#2ca02c'  # Green for second week
third_week_color = '#ff7f0e'  # Orange for third week
forth_week_color = '#fdff33'  # yellow for forth week
background_color = '#d3d3d3'  # Light grey for background
active_color = '#9467bd'  # Purple for active PCs
free_color = '#e377c2'  # Pink for free PCs

# Create progress bars
weeks = ['Semana 1 de julio', 'Semana 8 de julio', 'Semana 15 de julio', 'Semana 21 de julio']
progress = [first_week_progress, second_week_progress, third_week_progress, forth_week_progress]
colors = [first_week_color, second_week_color, third_week_color, forth_week_color]

for i, (week, prog, color) in enumerate(zip(weeks, progress, colors)):
    # Background bar (total target)
    ax.barh(i, total_pcs, color=background_color, alpha=0.3)
    
    # Progress bar
    ax.barh(i, prog, color=color, label=week)
    
    # Add text labels
    ax.text(prog + 0.5, i, f'{prog}/{total_pcs} ({prog/total_pcs*100:.1f}%)',
            va='center', fontweight='bold')

# Add sub-progress bars for active and free PCs
ax.barh(-1, active_pcs, color=active_color, alpha=0.7, height=0.3, label='PCs Activos')
ax.barh(-1, free_pcs, color=free_color, alpha=0.7, height=0.3, left=active_pcs, label='PCs Libres')

# Add text labels for sub-progress bars
ax.text(active_pcs/2, -1, f'Activos: {active_pcs}', ha='center', va='center', fontweight='bold', color='white')
ax.text(active_pcs + free_pcs/2, -1, f'Libres: {free_pcs}', ha='center', va='center', fontweight='bold', color='white')

# Customize the plot
ax.set_yticks(range(-1, len(weeks)))
ax.set_yticklabels(['Estado de PCs'] + weeks)
ax.set_xlabel('Número de PCs', fontsize=12)
ax.set_title('Progreso de Mantenimiento de PCs - Julio 2024', fontsize=14, fontweight='bold')

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add legend
ax.legend(loc='lower right')

plt.tight_layout()
plt.show()

# Print the progress data
print("Progreso de Mantenimiento de PCs:")
print("Semana | PCs con Mantenimiento | Progreso (%)")
print("-" * 50)
for week, prog in zip(weeks, progress):
    percentage = (prog / total_pcs) * 100
    print(f"{week} | {prog:2d} / {total_pcs} | {percentage:.2f}%")

print("\nEstado de PCs:")
print(f"PCs Activos: {active_pcs} ({active_pcs/total_pcs*100:.2f}%)")
print(f"PCs Libres: {free_pcs} ({free_pcs/total_pcs*100:.2f}%)")