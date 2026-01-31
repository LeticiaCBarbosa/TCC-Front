"""
generate_graphs.py
Generates publication-quality graphs for Neurodevice test results
"""

import matplotlib.pyplot as plt
import numpy as np

# Configure for publication quality
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'legend.fontsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.1
})

# Data from your test results
frequencies = [1, 5, 10, 20, 50, 100]
success_rates = [100, 100, 100, 100, 100, 100]  # All 100% in your latest test
latencies = [36.8, 24.5, 12.5, 17.0, 17.2, 13.4, 22.2, 15.9, 17.7, 17.2, 12.1, 17.8, 21.4, 13.3, 27.0]
intensities = list(range(30, 73, 3))  # 30% to 72% in steps of 3%

# ============================================
# GRAPH 1: Frequency Success Rate
# ============================================
plt.figure(figsize=(6, 4))

plt.plot(frequencies, success_rates, 'o-', color='#1f77b4', 
         linewidth=2, markersize=8, markerfacecolor='white',
         markeredgewidth=2, markeredgecolor='#1f77b4')

# Reference line
plt.axhline(y=100, color='red', linestyle='--', linewidth=1.5, 
            alpha=0.7, label='100% Reference')

plt.xlabel('Frequency (Hz)', fontweight='bold')
plt.ylabel('Success Rate (%)', fontweight='bold')
plt.title('Command Success Rate vs. Frequency', fontweight='bold', pad=15)
plt.grid(True, alpha=0.3, linestyle=':')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('frequency_success_rate.pdf')
plt.savefig('frequency_success_rate.png')
print("✓ Graph 1 saved: frequency_success_rate.pdf")

# ============================================
# GRAPH 2: Latency Distribution
# ============================================
plt.figure(figsize=(6, 4))

# Histogram
n, bins, patches = plt.hist(latencies, bins=6, edgecolor='black', 
                           color='#2ca02c', alpha=0.7, linewidth=1)

# Statistics lines
mean_latency = np.mean(latencies)
min_latency = min(latencies)
max_latency = max(latencies)

plt.axvline(x=mean_latency, color='red', linestyle='--', linewidth=2,
            label=f'Mean: {mean_latency:.1f} ms')
plt.axvline(x=min_latency, color='green', linestyle=':', linewidth=1.5,
            alpha=0.7, label=f'Min: {min_latency:.1f} ms')
plt.axvline(x=max_latency, color='orange', linestyle=':', linewidth=1.5,
            alpha=0.7, label=f'Max: {max_latency:.1f} ms')

# Shaded range
plt.axvspan(min_latency, max_latency, alpha=0.1, color='gray',
            label=f'Range: {max_latency-min_latency:.1f} ms')

plt.xlabel('Latency (ms)', fontweight='bold')
plt.ylabel('Frequency', fontweight='bold')
plt.title('Latency Distribution at 10 Hz', fontweight='bold', pad=15)
plt.grid(True, alpha=0.3, linestyle=':')
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('latency_distribution.pdf')
plt.savefig('latency_distribution.png')
print("✓ Graph 2 saved: latency_distribution.pdf")

# ============================================
# OPTIONAL GRAPH 3: Latency vs Intensity
# ============================================
plt.figure(figsize=(6, 4))

plt.plot(intensities, latencies, 's-', color='#9467bd', linewidth=2,
         markersize=6, markerfacecolor='white', markeredgewidth=2,
         markeredgecolor='#9467bd')

plt.xlabel('Stimulation Intensity (%)', fontweight='bold')
plt.ylabel('Latency (ms)', fontweight='bold')
plt.title('Latency vs. Stimulation Intensity', fontweight='bold', pad=15)
plt.grid(True, alpha=0.3, linestyle=':')

# Add regression line
z = np.polyfit(intensities, latencies, 1)
p = np.poly1d(z)
plt.plot(intensities, p(intensities), 'r--', alpha=0.5, linewidth=1.5,
         label=f'Trend: y = {z[0]:.3f}x + {z[1]:.1f}')

plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('latency_vs_intensity.pdf')
plt.savefig('latency_vs_intensity.png')
print("✓ Graph 3 saved: latency_vs_intensity.pdf")

print("\n" + "="*50)
print("✅ ALL GRAPHS GENERATED SUCCESSFULLY!")
print("="*50)
print("Files saved in current directory:")
print("1. frequency_success_rate.pdf")
print("2. latency_distribution.pdf")
print("3. latency_vs_intensity.pdf")
print("\n📝 Insert in Overleaf using:")
print(r"\includegraphics[width=0.8\linewidth]{filename.pdf}")

plt.show()