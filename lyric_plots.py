import embedding_model, embedding_plots
import sys

emb = embedding_model.EmbeddingModel(sys.argv[1])
emb.loadLabels("Model 0", "artist_ids.txt")
emb.loadLabels("Model 1", "word_ids.txt")
emplot = embedding_plots.EmbeddingPlots()
emplot.colors[0] = (1.0, 0.8, 0.8)
emplot.colors[1] = (0.8, 0.8, 1.0)
artist_axes = [-0.65, 1, -1, 0.75]
word_axes = [-2.43, 3.44, -2.52, 3.34]
artist_resolution = 0.05
word_resolution = 0.15

# artist label plots
a = artist_axes
emplot.axis(a[0], a[1], a[2], a[3])
emplot.plotComponent(emb, "Model 1")
emplot.plotComponent(emb, "Model 0", labels=True, resolution=artist_resolution)
figure = emplot.gcf()
figure.set_size_inches(24, 24)
emplot.saveFigure("artists.png")
emplot.clearPlot()

# word label plots
a = word_axes
emplot.axis(a[0], a[1], a[2], a[3])
emplot.plotComponent(emb, "Model 0")
emplot.plotComponent(emb, "Model 1", labels=True, resolution=word_resolution)
figure = emplot.gcf()
figure.set_size_inches(24, 24)
emplot.saveFigure("words.png")
emplot.clearPlot()
