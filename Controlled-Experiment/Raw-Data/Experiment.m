%% === 0. Load files ===
file_prompts = 'Data_Pseudonym.xlsx';

% Read sheets into tables
prompts = readtable(file_prompts, 'Sheet', 'Prompts');
logs = readtable(file_prompts, 'Sheet', 'Logs');
conversations = readtable(file_prompts, 'Sheet', 'Conversations');
usersTable = readtable(file_prompts, 'Sheet', 'Users');

%% === 1. Preprocessing ===
% Interpret enums as categorical variables
prompts = prompts(prompts.isSent == true, :);
% Define custom chat mode order (including 'Total')
prompts.chatMode = categorical(prompts.chatMode, [0 1 2], {'Energy efficient', 'Balanced', 'Performance'});

% Convert timestamps to datetime
prompts.sentAt = datetime(prompts.sentAt, 'InputFormat', 'yyyy-MM-dd''T''HH:mm:ss');
prompts.createdAt = datetime(prompts.createdAt, 'InputFormat', 'yyyy-MM-dd''T''HH:mm:ss');
%% === 2. Create new columns ===
prompts.responseLength = strlength(string(prompts.responseText));

%% === 3. Grouped evaluation (with all user-mode combos and totals) ===

% Get all unique users and all modes
allUsers = unique(prompts.userId);
allModes = categories(prompts.chatMode);

% Create full combination of users and modes
[U, M] = ndgrid(allUsers, allModes);
comboTable = table;
comboTable.userId = reshape(U, [], 1);
comboTable.chatMode = categorical(reshape(M, [], 1), allModes);

% Group actual data
G = findgroups(prompts.userId, prompts.chatMode);
T_actual = table;

T_actual.userId = splitapply(@(x) x(1), prompts.userId, G);
T_actual.chatMode = splitapply(@(x) x(1), prompts.chatMode, G);
T_actual.NumberOfPrompts = splitapply(@numel, prompts.id, G);
T_actual.InputTokens = splitapply(@sum, prompts.usage_numberOfInputTokens, G);
T_actual.OutputTokens = splitapply(@sum, prompts.usage_numberOfOutputTokens, G);
T_actual.TotalUsageWh = splitapply(@sum, prompts.usage_usageInWh, G);
T_actual.TotalUsageWhCorrected = splitapply(@sum, prompts.usageInWhCorrected, G);

% Join full combination with actual data to ensure 0s are included
T = outerjoin(comboTable, T_actual, ...
    'Keys', {'userId', 'chatMode'}, ...
    'MergeKeys', true);

% Replace NaNs with 0 for numeric columns
T.NumberOfPrompts(isnan(T.NumberOfPrompts)) = 0;
T.InputTokens(isnan(T.InputTokens)) = 0;
T.OutputTokens(isnan(T.OutputTokens)) = 0;
T.TotalUsageWh(isnan(T.TotalUsageWh)) = 0;
T.TotalUsageWhCorrected(isnan(T.TotalUsageWhCorrected)) = 0;

% Add total row per user
G_user = findgroups(T.userId);
T_userTotal = table;
T_userTotal.userId = splitapply(@(x) x(1), T.userId, G_user);
T_userTotal.chatMode = categorical(repmat("Total", height(T_userTotal), 1), ...
    [allModes; "Total"]);
T_userTotal.NumberOfPrompts = splitapply(@sum, T.NumberOfPrompts, G_user);
T_userTotal.InputTokens = splitapply(@sum, T.InputTokens, G_user);
T_userTotal.OutputTokens = splitapply(@sum, T.OutputTokens, G_user);
T_userTotal.TotalUsageWh = splitapply(@sum, T.TotalUsageWh, G_user);
T_userTotal.TotalUsageWhCorrected = splitapply(@sum, T.TotalUsageWhCorrected, G_user);

% Combine mode rows and total rows
T = [T; T_userTotal];

% Sort nicely by user, then mode
T = sortrows(T, {'userId', 'chatMode'});

% Add % column (only for modes, not total)
% Compute total prompts per user (one row per user)
userTotalPrompts = groupsummary(T, "userId", "max", "NumberOfPrompts");
userTotalPrompts.Properties.VariableNames{'max_NumberOfPrompts'} = 'TotalPromptsPerUser';

% Join this summary back into T
T = outerjoin(T, userTotalPrompts(:, {'userId', 'TotalPromptsPerUser'}), ...
    'Keys', 'userId', 'MergeKeys', true);
T.PctPromptsPerUserMode = 100 * (T.NumberOfPrompts ./ T.TotalPromptsPerUser);
T.TotalPromptsPerUser = [];  % Remove helper column from final table

T.PctPromptsPerUserMode(T.chatMode == "Total") = 100; % blank for totals

%% === 4. Display grouped results ===
disp(T);

%% === 5. Plot: Number of prompts per mode ===
figure('Name','Prompts per Mode');
modes = categories(T.chatMode);
counts = zeros(numel(modes),1);
for i = 1:numel(modes)
    counts(i) = sum(T.NumberOfPrompts(T.chatMode == modes{i}));
end
bar(categorical(modes), counts);
ylabel('Number of Prompts');
title('Total Prompts per Mode');
grid on;

%% === 6. Plot: Energy usage per user and mode ===
figure('Name','Energy Usage per User and Mode');
barData = unstack(T(:, {'userId', 'chatMode', 'TotalUsageWh'}), 'TotalUsageWh', 'chatMode');
bar(categorical(barData.userId), barData{:,2:end});
xlabel('User ID');
ylabel('Energy Usage (Wh)');
title('Total Energy Usage per User & Mode');
legend(barData.Properties.VariableNames(2:end), 'Location', 'northwest');
grid on;

%% === 11. Display final table ===
disp('Evaluation per User and Mode:');
disp(T);

%% === 12. Aggregated evaluation per mode ===
[Gm, modes] = findgroups(T.chatMode);
Agg = table;

Agg.chatMode = modes;
Agg.InputTokens = splitapply(@sum, T.InputTokens, Gm);
Agg.OutputTokens = splitapply(@sum, T.OutputTokens, Gm);
Agg.TotalUsageWh = splitapply(@sum, T.TotalUsageWh, Gm);
Agg.TotalUsageWhCorrected = splitapply(@sum, T.TotalUsageWhCorrected, Gm);
Agg.TotalPrompts = splitapply(@sum, T.NumberOfPrompts, Gm);

% Calculate total prompts and total energy usage (use MAX because every
% mode also has a total)
totalPromptsAll = max(Agg.TotalPrompts);
totalWhAll = max(Agg.TotalUsageWh);
totalWhCorrectedAll = max(Agg.TotalUsageWhCorrected);

% Calculate percentage columns
Agg.PctPromptsPerMode = (Agg.TotalPrompts ./ totalPromptsAll) * 100;
Agg.PctUsagePerMode = (Agg.TotalUsageWh ./ totalWhAll) * 100;
Agg.PctUsageCorrectedPerMode = (Agg.TotalUsageWhCorrected ./ totalWhCorrectedAll) * 100;

disp('Aggregated values per Mode:');
disp(Agg);

%% === Prompts per User and Day (Split by Mode and Total) ===
% Group by userId, day, and chatMode
G = findgroups(prompts.userId, prompts.day, prompts.chatMode);
summaryTable = table;
summaryTable.userId = splitapply(@(x) x(1), prompts.userId, G);
summaryTable.day = splitapply(@(x) x(1), prompts.day, G);
summaryTable.chatMode = splitapply(@(x) x(1), prompts.chatMode, G);
summaryTable.numPrompts = splitapply(@numel, prompts.id, G);

% Get all unique combinations
users = unique(prompts.userId);
days = unique(prompts.day);
modes = categories(prompts.chatMode);

% Generate variable names for each day-mode and day-total
varNames = {};
for d = days'
    for m = modes'
        varNames{end+1} = sprintf('Day%d_%s', d, matlab.lang.makeValidName(char(m)));
    end
    varNames{end+1} = sprintf('Day%d_Total', d);
end

% Initialize result table
result = array2table(zeros(numel(users), numel(varNames)), ...
    'VariableNames', varNames);
result.userId = users;

% Fill in prompt counts per user/day/mode
for i = 1:height(summaryTable)
    uid = summaryTable.userId(i);
    day = summaryTable.day(i);
    mode = summaryTable.chatMode(i);
    n = summaryTable.numPrompts(i);

    rowIdx = find(result.userId == uid);
    colName = sprintf('Day%d_%s', day, matlab.lang.makeValidName(char(mode)));
    result{rowIdx, colName} = result{rowIdx, colName} + n;

    % Update total
    totalCol = sprintf('Day%d_Total', day);
    result{rowIdx, totalCol} = result{rowIdx, totalCol} + n;
end

% Move userId to the front
result = movevars(result, 'userId', 'Before', 1);

% Display result
disp('Prompt Matrix per User, Day, and Mode with Totals:');
disp(result);

%% === Prompts per User and Day ===
% Group prompts by userId and day, count number of prompts
G_day = findgroups(prompts.userId, prompts.day);
userDayTable = table;

userDayTable.userId = splitapply(@(x) x(1), prompts.userId, G_day);
userDayTable.day = splitapply(@(x) x(1), prompts.day, G_day);
userDayTable.NumberOfPrompts = splitapply(@numel, prompts.id, G_day);

% Display the table
disp('Number of prompts per User and Day:');
disp(userDayTable);

% Unique users and days
users = unique(userDayTable.userId);
days = unique(userDayTable.day);

% Build prompt matrix: rows = users, columns = days
promptMatrix = zeros(numel(users), numel(days));
for i = 1:numel(users)
    for j = 1:numel(days)
        idx = userDayTable.userId == users(i) & userDayTable.day == days(j);
        if any(idx)
            promptMatrix(i,j) = userDayTable.NumberOfPrompts(idx);
        end
    end
end

% === Grouped Bar Chart: Per User (X) and Day (grouped bars) ===
figure('Name','Prompts per User and Day (Bar Chart)');
bar(users, promptMatrix, 'grouped');
xlabel('User ID');
ylabel('Number of Prompts');
title('Number of Prompts per User and Day');
legend(arrayfun(@(d) sprintf('Day %d', d), days, 'UniformOutput', false), ...
       'Location', 'northeastoutside');
grid on;

% === Line Chart: Per User (X) and Day (one line per day) ===
figure('Name', 'Prompts per User and Day (Line Chart)');
hold on;

for j = 1:numel(days)
    plot(users, promptMatrix(:,j), '-o', 'DisplayName', sprintf('Day %d', days(j)));
end

% Plot average across days
avgPrompts = mean(promptMatrix, 2);
plot(users, avgPrompts, '-k', 'LineWidth', 2, 'DisplayName', 'Average');

xlabel('User ID');
ylabel('Number of Prompts');
title('Number of Prompts per User and Day with Average');
legend('Location', 'northeastoutside');
grid on;
hold off;



%% === Plot: Chat Mode Usage per Day ===

% Group by day and chat mode
G_dayMode = findgroups(prompts.day, prompts.chatMode);
modeDayTable = table;
modeDayTable.day = splitapply(@(x) x(1), prompts.day, G_dayMode);
modeDayTable.chatMode = splitapply(@(x) x(1), prompts.chatMode, G_dayMode);
modeDayTable.NumberOfPrompts = splitapply(@numel, prompts.id, G_dayMode);

% Prepare matrix: rows = days, columns = modes
days = unique(modeDayTable.day);
modes = categories(prompts.chatMode);
modeMatrix = zeros(numel(days), numel(modes));

for i = 1:numel(days)
    for j = 1:numel(modes)
        idx = (modeDayTable.day == days(i)) & (modeDayTable.chatMode == modes{j});
        if any(idx)
            modeMatrix(i, j) = modeDayTable.NumberOfPrompts(idx);
        else
            modeMatrix(i, j) = 0;
        end
    end
end

% Plot stacked bar chart
figure('Name','Chat Mode Usage per Day');
bar(days, modeMatrix, 'stacked');
xlabel('Day');
ylabel('Number of Prompts');
title('Chat Mode Usage per Day');
legend(modes, 'Location', 'northeastoutside');
grid on;

%% === Plot: Chat Mode Usage per Day (Percentage) ===

% Normalize modeMatrix to percentages
modeMatrixPct = modeMatrix ./ sum(modeMatrix, 2) * 100;

% Handle potential division by zero (in case a day has no prompts)
modeMatrixPct(isnan(modeMatrixPct)) = 0;

% Plot stacked percentage bar chart
figure('Name','Chat Mode Usage per Day (Percentage)');
bar(days, modeMatrixPct, 'stacked');
xlabel('Day');
ylabel('Percentage of Prompts');
title('Chat Mode Usage per Day (Percentage)');
legend(modes, 'Location', 'northeastoutside');
grid on;

%% === Load metrics ===
metrics = logs(strcmp(logs.message, '/metrics'), :);

%% === Convert datetime day to numeric weekday 1=Monday ... 5=Friday ===
wday = weekday(metrics.day); 
wday_adj = wday - 1;      % Monday=1 ... Sunday=0
wday_adj(wday_adj == 0) = 7; % Sunday=7

% Keep only Monday to Friday
validDaysIdx = wday_adj >= 1 & wday_adj <= 5;
metrics = metrics(validDaysIdx, :);
metrics.dayNum = wday_adj(validDaysIdx);

%% === Prepare full user-day grid (all users × days 1 to 5) ===
days = (1:5)';
[U, D] = ndgrid(allUsers, days);
combo = table;
combo.userId = reshape(U, [], 1);
combo.dayNum = reshape(D, [], 1);

%% === Group metrics by userId and dayNum ===
G = findgroups(metrics.userId, metrics.dayNum);
T_visits = table;
T_visits.userId = splitapply(@(x) x(1), metrics.userId, G);
T_visits.dayNum = splitapply(@(x) x(1), metrics.dayNum, G);
T_visits.PageVisits = splitapply(@numel, metrics.message, G);

%% === Outer join full grid with actual counts ===
T_full = outerjoin(combo, T_visits, ...
    'Keys', {'userId', 'dayNum'}, ...
    'MergeKeys', true);

% Replace missing visits with zero
T_full.PageVisits(isnan(T_full.PageVisits)) = 0;

%% === Pivot to wide format: one row per user, columns Day1...Day5 ===
T_wide = unstack(T_full, 'PageVisits', 'dayNum', 'VariableNamingRule', 'preserve');

% Rename columns for clarity
dayCols = strcat("Day", string(days));
T_wide.Properties.VariableNames(2:end) = dayCols;

%% === Display result ===
disp('Page Visits per Day and User (Monday=1 to Friday=5):');
disp(T_wide);
