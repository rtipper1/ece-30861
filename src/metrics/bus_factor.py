"""
bus_factor.py
---------------
Bus Factor Metric.

Summary
- Calculates contributor redundancy relative to project size.
- Uses number of contributors per parameter scale as described in the rubric.
- Scores in [0,1]; higher = safer (more maintainers).

Notes
- Determine with: git shortlog -s -n 
- lists contributor and number of commits
"""
