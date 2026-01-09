# Emergency Dispatch System

A self-contained Python system for processing emergency calls with emotion detection, fact extraction, and triage scoring.

## Overview

This system processes emergency call transcripts and provides:
- **Emotion Detection**: Classifies caller emotion and severity
- **Fact Extraction**: Extracts key information (location, hazards, injuries, etc.)
- **Triage Scoring**: Assigns priority scores based on emotion and facts
- **Dispatcher Assistance**: Provides AI suggestions and calm-down strategies
- **Evaluation Metrics**: Calculates system performance metrics

## Project Structure

```
.
├── main.py                 # Main entry point
├── emotion_detection.py    # Emotion detection module
├── fact_extraction.py      # Fact extraction module
├── triage_scoring.py       # Triage scoring module
├── policy_gate.py          # Policy gate module
├── dispatcher_assistance.py # Dispatcher assistance module
├── process_call.py         # Call processing pipeline
├── evaluation.py           # Evaluation metrics
├── visualization.py        # Visualization functions
├── data.py                 # Data loading functions
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Main Script

```bash
python main.py
```

This will:
1. Load dummy emergency calls
2. Process all calls through the pipeline
3. Display summary results
4. Show dispatch priority queue
5. Print detailed analysis for each call
6. Calculate evaluation metrics
7. Generate visualizations (if matplotlib is available)

### Using Individual Modules

#### Process a Single Call

```python
from data import get_dummy_calls
from process_call import process_call, print_call_details

# Get a call
calls = get_dummy_calls()
call = calls[0]

# Process the call
result = process_call(call)

# Print details
print_call_details(call, result)
```

#### Emotion Detection

```python
from emotion_detection import detect_emotion, classify_emotion_class, get_severity_band

transcript = "Oh my god, there's blood everywhere! Please help!"
score = detect_emotion(transcript)
emotion_class = classify_emotion_class(score)
severity_band = get_severity_band(score)

print(f"Emotion Score: {score}")
print(f"Emotion Class: {emotion_class}")
print(f"Severity Band: {severity_band}")
```

#### Fact Extraction

```python
from fact_extraction import extract_facts

transcript = "There has been a crash near highway 6. Two cars. One driver not moving."
facts = extract_facts(transcript)

print(facts)
```

#### Triage Scoring

```python
from emotion_detection import detect_emotion
from fact_extraction import extract_facts
from triage_scoring import final_triage, get_triage_label

transcript = "There has been a crash near highway 6. Two cars. One driver not moving."
emotion_score = detect_emotion(transcript)
facts = extract_facts(transcript)

triage_score = final_triage(emotion_score, facts)
triage_label = get_triage_label(triage_score)

print(f"Triage Score: {triage_score}")
print(f"Triage Label: {triage_label}")
```

#### Dispatcher Assistance

```python
from dispatcher_assistance import get_ui_suggestions
from emotion_detection import detect_emotion
from fact_extraction import extract_facts

call = {
    "call_id": "A317",
    "transcript": "There has been a crash near highway 6. Two cars. One driver not moving.",
    "asr_conf": 0.92,
    "llm_conf": 0.81,
}

emotion_score = detect_emotion(call["transcript"])
facts = extract_facts(call["transcript"])
ui = get_ui_suggestions(call, facts, emotion_score)

print(ui)
```

## Module Documentation

### emotion_detection.py

Functions:
- `detect_emotion(transcript: str) -> float`: Detect emotion severity score (1-5)
- `classify_emotion_class(emotion_score: float) -> str`: Classify emotion class
- `get_severity_band(emotion_score: float) -> str`: Get severity band
- `get_emotion_class_info(emotion_class: str) -> Dict`: Get emotion class info
- `get_severity_band_info(severity_band: str) -> Tuple`: Get severity band range

### fact_extraction.py

Functions:
- `extract_facts(transcript: str) -> Dict[str, Any]`: Extract structured facts
- `has_critical_hazards(facts: Dict[str, Any]) -> bool`: Check for critical hazards
- `has_life_threatening_injuries(facts: Dict[str, Any]) -> bool`: Check for life-threatening injuries
- `get_vehicle_count(facts: Dict[str, Any]) -> int`: Get vehicle count

### triage_scoring.py

Functions:
- `triage_from_facts(facts: Dict) -> float`: Calculate triage score from facts
- `final_triage(emotion_score: float, facts: Dict) -> float`: Final triage score
- `get_triage_label(triage_score: float) -> str`: Get triage label
- `get_triage_label_info(triage_label: str) -> Dict`: Get triage label info

### policy_gate.py

Functions:
- `policy_gate(asr_conf: float, llm_conf: float, asr_threshold: float = None, llm_threshold: float = None) -> bool`: Check if gate passes
- `get_default_thresholds() -> Dict[str, float]`: Get default thresholds

### dispatcher_assistance.py

Functions:
- `get_ui_suggestions(call: Dict[str, Any], facts: Dict[str, Any], emotion_score: float) -> Dict[str, Any]`: Get UI suggestions
- `get_checklist_items() -> List[str]`: Get checklist items
- `get_prompt_templates() -> Dict[str, str]`: Get prompt templates
- `calculate_dispatch_time(triage_label: str, gate_ok: bool) -> int`: Calculate dispatch time

### process_call.py

Functions:
- `process_call(call: Dict[str, Any]) -> Dict[str, Any]`: Process a single call
- `get_call_details(call: Dict[str, Any], processed_result: Dict[str, Any] = None) -> str`: Get call details string
- `print_call_details(call: Dict[str, Any], processed_result: Dict[str, Any] = None) -> None`: Print call details

### evaluation.py

Functions:
- `calculate_metrics(df_results: pd.DataFrame) -> Dict[str, Any]`: Calculate evaluation metrics
- `print_metrics(metrics: Dict[str, Any]) -> None`: Print metrics
- `get_accuracy_metrics(df_results: pd.DataFrame, ground_truth: pd.DataFrame = None) -> Dict[str, float]`: Get accuracy metrics

### visualization.py

Functions:
- `plot_emotion_distribution(df: pd.DataFrame, save_path: Optional[str] = None) -> None`: Plot emotion distribution
- `plot_triage_distribution(df: pd.DataFrame, save_path: Optional[str] = None) -> None`: Plot triage distribution
- `plot_emotion_vs_triage(df: pd.DataFrame, save_path: Optional[str] = None) -> None`: Plot emotion vs triage
- `plot_triage_labels(df: pd.DataFrame, save_path: Optional[str] = None) -> None`: Plot triage labels
- `plot_all_visualizations(df: pd.DataFrame, save_dir: Optional[str] = None) -> None`: Plot all visualizations

### data.py

Functions:
- `get_dummy_calls() -> List[Dict[str, Any]]`: Get dummy call data
- `load_calls_from_file(file_path: str) -> List[Dict[str, Any]]`: Load calls from JSON file
- `save_calls_to_file(calls: List[Dict[str, Any]], file_path: str) -> None`: Save calls to JSON file
- `validate_call(call: Dict[str, Any]) -> bool`: Validate call dictionary

## Data Format

### Call Dictionary

```python
{
    "call_id": "A317",
    "transcript": "There has been a crash near highway 6...",
    "asr_conf": 0.92,
    "llm_conf": 0.81,
    "bg_noise": "siren",
    "timestamp": "2024-10-15 14:32:15",
}
```

### Processed Result Dictionary

```python
{
    "call_id": "A317",
    "emotion_score": 4.8,
    "emotion_class": "panicked",
    "severity_band": "critical",
    "triage_score": 4.8,
    "triage_label": "CRITICAL",
    "gate_ok": True,
    "num_ai_suggestions": 0,
    "has_calm_strategies": True,
    "dispatch_time_s": 1,
    "facts": {...},
    "ui_suggestions": {...}
}
```

## Examples

See the `main.py` script for a complete example of processing calls and generating reports.

## License

This project is for educational purposes.

## Author

Gaurangi Sinha - IUI Project

