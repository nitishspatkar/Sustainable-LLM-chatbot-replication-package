# Data Dictionary

Comprehensive reference for all data fields, variables, and formats used in the sustainable AI chatbot research study.

## 📊 Survey Data Dictionary

### **Demographics Variables**

| Variable | Type | Description | Values |
|----------|------|-------------|---------|
| `Q1` | Categorical | Technical proficiency level | Beginner, Intermediate, Advanced, Expert |
| `Q2` | Categorical | Age group | 18-24, 25-34, 35-44, 45-54, 55-64, 65+ |
| `Q3` | Categorical | Professional role | Student, Software Developer/Engineer, Data Scientist/Analyst, Researcher/Academic, Business Professional, Other |
| `Q4` | Categorical | Business domain | Technology, Healthcare, Finance, Education, Government, Other |

### **Usage Pattern Variables**

| Variable | Type | Description | Values |
|----------|------|-------------|---------|
| `Q5` | Multi-select | AI services used | ChatGPT, Claude, Gemini, Copilot, Other, None |
| `Q6` | Categorical | Usage frequency | Daily, Several times a week, Weekly, Monthly, Rarely, Never |
| `Q7` | Categorical | Daily usage time | Less than 30 minutes, 30 minutes to 1 hour, 1-2 hours, 2-4 hours, More than 4 hours |
| `Q8` | Multi-select | Primary reasons for using AI | Research and information gathering, Creative writing and content generation, Code development and programming, Data analysis and visualization, Learning and education, Other |
| `Q9` | Categorical | Preferred AI service | ChatGPT, Claude, Gemini, Copilot, Other, No preference |
| `Q10` | Categorical | Usage context | Work/Professional, Personal projects, Learning/Education, Research, Creative pursuits, Other |

### **Environmental Attitude Variables (Likert Scales)**

| Variable | Type | Scale | Description | Values |
|----------|------|-------|-------------|---------|
| `Q11` | Ordinal | Concern Scale | Environmental impact concern | 1: Not at all concerned, 2: Slightly concerned, 3: Moderately concerned, 4: Very concerned, 5: Extremely concerned |
| `Q15` | Ordinal | Agreement Scale | Energy optimization agreement | 1: Strongly disagree, 2: Disagree, 3: Neither agree nor disagree, 4: Agree, 5: Strongly agree |
| `Q16` | Ordinal | Agreement Scale | Eco-friendly preference agreement | 1: Strongly disagree, 2: Disagree, 3: Neither agree nor disagree, 4: Agree, 5: Strongly agree |
| `Q17` | Ordinal | Importance Scale | Environmental impact importance | 1: Not at all important, 2: Slightly important, 3: Moderately important, 4: Very important, 5: Extremely important |
| `Q18` | Ordinal | Preference Scale | Eco-friendly mode preference | 1: Definitely not, 2: Probably not, 3: Maybe, 4: Probably yes, 5: Definitely yes |
| `Q19` | Ordinal | Preference Scale | Energy information preference | 1: Definitely not, 2: Probably not, 3: Maybe, 4: Probably yes, 5: Definitely yes |
| `Q20` | Ordinal | Importance Scale | Energy optimization importance | 1: Not at all important, 2: Slightly important, 3: Moderately important, 4: Very important, 5: Extremely important |
| `Q21` | Ordinal | Preference Scale | Energy information influence | 1: Definitely not, 2: Probably not, 3: Maybe, 4: Probably yes, 5: Definitely yes |

### **Open-ended Variables**

| Variable | Type | Description | Content |
|----------|------|-------------|---------|
| `Q22` | Text | Sustainability suggestions | Free-text responses about AI sustainability improvements |
| `Q23` | Text | Environmental concerns | Free-text responses about AI environmental concerns |
| `Q24` | Text | Usage optimization ideas | Free-text responses about optimizing AI usage |
| `Q25` | Text | Policy recommendations | Free-text responses about AI sustainability policies |
| `Q26` | Text | Technical improvements | Free-text responses about technical AI improvements |
| `Q27` | Text | User interface preferences | Free-text responses about UI preferences |
| `Q28` | Text | Additional comments | Free-text responses with additional comments |
| `Q29` | Text | Other thoughts | Free-text responses about AI optimization |

## 🔬 Experiment Data Dictionary

### **User Data**

| Variable | Type | Description | Format |
|----------|------|-------------|---------|
| `userId` | String | Unique participant identifier | UUID format |
| `name` | String | Participant email/identifier | Email format |
| `identity` | String | Participant identity | Email format |
| `enableSustainabiltyFeatures` | Boolean | Sustainability features enabled | true/false |
| `mode` | Integer | Assigned chat mode | 0, 1, 2 |
| `energyUnitId` | String | Energy unit identifier | String ID |
| `createdAt` | DateTime | Account creation timestamp | ISO 8601 format |

### **Chat Mode Data**

| Variable | Type | Description | Values |
|----------|------|-------------|---------|
| `chatMode` | Integer | Chat mode identifier | 0: Energy Efficient, 1: Balanced, 2: Performance |
| `name` | String | Mode display name | "Energy Efficient Mode", "Balanced Mode", "Performance Mode" |
| `icon` | String | Mode icon identifier | "energy_savings_leaf", "balance", "speed" |
| `modelName` | String | AI model used | "gpt-4.1-nano", "gpt-4o-mini", "gpt-4o" |
| `historyLimit` | Integer | Conversation history limit | 2, 5, 10 turns |
| `alphaWhPerInputToken` | Float | Energy per input token | 0.00007, 0.0001, 0.00017 Wh |
| `betaWhPerOutputToken` | Float | Energy per output token | 0.00021, 0.0003, 0.00051 Wh |
| `zetaConstWh` | Float | Constant overhead energy | 0.025, 0.03 Wh |

### **Prompt/Response Data**

| Variable | Type | Description | Format |
|----------|------|-------------|---------|
| `id` | String | Unique prompt identifier | UUID format |
| `userId` | String | Participant identifier | UUID format |
| `chatMode` | Integer | Chat mode used | 0, 1, 2 |
| `promptText` | String | User prompt text | Free text |
| `responseText` | String | AI response text | Free text |
| `responseLength` | Integer | Response text length | Character count |
| `isSent` | Boolean | Whether prompt was sent | true/false |
| `sentAt` | DateTime | Prompt sent timestamp | ISO 8601 format |
| `createdAt` | DateTime | Prompt created timestamp | ISO 8601 format |

### **Usage/Energy Data**

| Variable | Type | Description | Units |
|----------|------|-------------|-------|
| `usage_numberOfInputTokens` | Integer | Number of input tokens | Token count |
| `usage_numberOfOutputTokens` | Integer | Number of output tokens | Token count |
| `usage_usageInWh` | Float | Energy consumption | Watt-hours |
| `usageInWhCorrected` | Float | Corrected energy consumption | Watt-hours |
| `usage_usageInWhPerInputToken` | Float | Energy per input token | Wh/token |
| `usage_usageInWhPerOutputToken` | Float | Energy per output token | Wh/token |

### **Log Data**

| Variable | Type | Description | Format |
|----------|------|-------------|---------|
| `id` | String | Log entry identifier | UUID format |
| `type` | Integer | Log entry type | 1, 2, 3, etc. |
| `message` | String | Log message | Free text |
| `userId` | String | Participant identifier | UUID format |
| `createdAt` | DateTime | Log timestamp | ISO 8601 format |

### **Conversation Data**

| Variable | Type | Description | Format |
|----------|------|-------------|---------|
| `id` | String | Conversation identifier | UUID format |
| `userId` | String | Participant identifier | UUID format |
| `chatMode` | Integer | Chat mode used | 0, 1, 2 |
| `startedAt` | DateTime | Conversation start time | ISO 8601 format |
| `endedAt` | DateTime | Conversation end time | ISO 8601 format |
| `messageCount` | Integer | Number of messages | Count |
| `totalTokens` | Integer | Total tokens used | Token count |
| `totalEnergy` | Float | Total energy consumed | Watt-hours |

## 📈 Analysis Variables

### **Aggregated Metrics**

| Variable | Type | Description | Calculation |
|----------|------|-------------|-------------|
| `NumberOfPrompts` | Integer | Prompts per user-mode combination | Count aggregation |
| `InputTokens` | Integer | Total input tokens | Sum aggregation |
| `OutputTokens` | Integer | Total output tokens | Sum aggregation |
| `TotalUsageWh` | Float | Total energy consumption | Sum aggregation |
| `TotalUsageWhCorrected` | Float | Corrected total energy | Sum aggregation |
| `AverageTokensPerPrompt` | Float | Average tokens per prompt | Mean calculation |
| `AverageEnergyPerPrompt` | Float | Average energy per prompt | Mean calculation |
| `EnergyEfficiency` | Float | Energy per token ratio | Energy/tokens |

### **Theme Analysis Variables**

| Variable | Type | Description | Values |
|----------|------|-------------|---------|
| `Theme` | String | Sustainability theme | Infrastructure/Green Energy, Alternative Solutions, Model/Algorithm Efficiency, Policy/Tax/Offsets, Pricing/Responsibility, Awareness/Transparency, Bias/Social Impact, Usage Scope/Limitations |
| `Count` | Integer | Theme frequency | Count of responses |
| `Percentage` | Float | Theme percentage | Percentage of total responses |
| `Quote` | String | Representative quote | Sample response text |

## 🔧 Data Processing Notes

### **Data Cleaning**
- **Missing Values**: Handled with appropriate imputation or exclusion
- **Outliers**: Identified and handled based on statistical criteria
- **Data Validation**: Cross-validation of related variables
- **Format Standardization**: Consistent formatting across all variables

### **Data Transformation**
- **Likert Scale Processing**: Automatic detection and proper labeling
- **Token Calculation**: Standardized token counting algorithms
- **Energy Calculation**: Consistent energy consumption formulas
- **Aggregation**: Appropriate aggregation methods for different metrics

### **Data Quality**
- **Completeness**: Percentage of non-missing values
- **Consistency**: Cross-variable validation checks
- **Accuracy**: Validation against known standards
- **Reliability**: Test-retest reliability measures

---

**Data dictionary maintained for research reproducibility** 🌱
