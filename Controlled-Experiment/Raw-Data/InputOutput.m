% Load Excel data
file = 'Data_Pseudonym.xlsx';
sheet = 'Prompts';
data = readtable(file, 'Sheet', sheet);

% Extract input and output tokens
x = data.usage_numberOfInputTokens;
y = data.usage_numberOfOutputTokens;

% Filter out invalid entries
valid = ~isnan(x) & ~isnan(y) & x > 0 & y > 0;
x = x(valid);
y = y(valid);

% Sort by input tokens for smooth plotting
[x_sorted, idx] = sort(x);
y_sorted = y(idx);

% LOWESS smoothing to reveal real relationship
y_smooth = smooth(x_sorted, y_sorted, 0.05, 'lowess');  % 0.05 = smoothing span (adjust as needed)

% Reference line y = x
y_ref = x_sorted;

% Optional: Crop axes to the 95th percentile to avoid outliers
x_max = prctile(x, 95);
y_max = prctile(y, 94.83); % Skip one point to clean the graph image

% Plot
figure;
scatter(x, y, 10, 'filled', 'MarkerFaceAlpha', 0.3);
hold on;
plot(x_sorted, y_smooth, 'b-', 'LineWidth', 2);      % LOWESS trend
plot(x_sorted, y_ref, 'g--', 'LineWidth', 1.5);       % y = x reference

% Formatting
xlim([0, x_max]);
ylim([0, y_max]);
xlabel('Input Tokens');
ylabel('Output Tokens');
title('Smoothed Relation between Input and Output Tokens');
legend('Prompt Data', 'LOWESS Smoothed', 'y = x', 'Location', 'southeast');
grid on;
