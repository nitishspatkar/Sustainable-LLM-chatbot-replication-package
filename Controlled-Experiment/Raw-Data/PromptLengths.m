% Load Excel file and sheet
file = 'Data.xlsx';  % Adjust path if needed
sheet = 'Prompts';

% Read the table
data = readtable(file, 'Sheet', sheet, 'ReadVariableNames', true);
lengthsRaw = data.promptTextHistoryLengths;
numPrompts = height(data);

% Number of interpolation points (e.g., representing 0–100%)
nInterp = 100;

% Matrix to store all normalized prompt curves
normalizedCurves = NaN(numPrompts, nInterp);

row = 1; % Row counter for valid prompts

for i = 1:numPrompts
    % Convert string to numeric array
    str = lengthsRaw{i};
    nums = sscanf(str, '%d,', Inf); % read comma-separated values
    if isempty(nums)
        parts = split(str, ',');
        nums = str2double(parts);
    end
    nums = nums(:)'; % ensure row vector

    % Skip if not enough points for interpolation
    if length(nums) < 2
        continue;
    end

    % Normalize x-values to range [0, 1] (prompt progress)
    steps = linspace(0, 1, length(nums));

    % Normalize y-values to final length (range [0, 1])
    finalLen = nums(end);
    if finalLen == 0 || any(isnan(nums))
        continue;
    end
    yNorm = nums / finalLen;

    % Interpolate to a fixed number of x-values (0–1 scale)
    xInterp = linspace(0, 1, nInterp);
    yInterp = interp1(steps, yNorm, xInterp, 'linear', 'extrap');

    % Store in matrix
    normalizedCurves(row, :) = yInterp;
    row = row + 1;
end

% Compute average curve across prompts
meanCurve = nanmean(normalizedCurves, 1);

% Smooth the average curve (optional)
smoothCurve = smooth(meanCurve, 0.2, 'loess'); % 0.2 = smoothing factor

% Plot
figure;
plot(linspace(0, 100, nInterp), smoothCurve * 100, 'LineWidth', 2);
xlabel('Prompt progress [%]');
ylabel('Text length [% of final length]');
title('Average normalized prompt growth curve');
grid on;

% Optional: show how many prompts were used
fprintf('Used prompts: %d of %d\n', row-1, numPrompts);
