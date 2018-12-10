## Ideas

### Data structure
Each record contains at least one label.
```
{
  "content": "A piece of text that needs to be processed",
  "labels": {
    "category": "business/sport/politics etc."
    "emotions": "positive/negative/neutral"
    "language": "official/urban"
  }
}
```
Each record contains at least one label.

### Predicting process
Many models, each one recognizes one label (category, emotions, language). Models are automatically learned and added
to "Prediction chain" when new label is found.

### Presentation
Chrome extension. When selecting any text it predict its labels.

### Clustering
Data from https://newsapi.org/