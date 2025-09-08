
# Energy Consumption Analysis Report

## Summary Statistics
- Total Prompts Analyzed: 286
- Total Energy Consumed: 194.3859 Wh
- Average Energy per Prompt: 0.682056 Wh

## Mode Comparison
                 usageInWh                          total_tokens            energy_per_token        
                     count    mean     std      sum         mean        std             mean     std
mode_name                                                                                           
Balanced                57  0.6517  0.6595  37.1450    3001.5088  4024.9912           0.0003  0.0002
Energy Efficient       156  0.3723  0.3285  58.0839    1766.6923  1318.0865           0.0002  0.0001
Performance             72  1.3772  0.8163  99.1570    3525.0000  2342.4640           0.0004  0.0001

## Key Findings
1. **Energy Efficient Mode** shows the lowest energy consumption per prompt
2. **Performance Mode** shows the highest energy consumption per prompt
3. **Balanced Mode** provides a middle ground between efficiency and performance

## Files Generated
- Energy consumption charts: `plots/energy_consumption_by_mode.png`
- Token efficiency charts: `plots/token_efficiency_comparison.png`
- Input/output scatter: `plots/input_output_token_scatter.png`
- Energy distribution: `plots/energy_distribution_by_mode.png`
- Analysis data: `data/mode_energy_analysis.csv`, `data/token_efficiency_analysis.csv`

## Methodology
- Energy consumption calculated using token-based modeling
- Analysis based on 286 valid prompts
- Statistical analysis performed using pandas and matplotlib
- Charts optimized for publication quality

Generated on: 2025-09-05 16:45:54
