# Architecture

```text
Synthetic Traffic Generator
          |
          v
     Flow Collector/API
          |
          v
   Feature Extraction
          |
   +------+------+------+
   |             |      |
 Rules       Anomaly    ML
 Engine      Detector  Model
   |             |      |
   +------+------+------+
          |
          v
     Hybrid Risk Engine
          |
          v
      Alert Engine
          |
          v
        SQLite
          |
          v
     React SOC UI
          |
          v
       Analyst
```
