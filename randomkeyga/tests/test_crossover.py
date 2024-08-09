from randomkeyga import optimizer
import numpy as np

def test_onepointcrossover():
    chsize = 10
    ch1 = optimizer.Chromosome(chsize)
    ch2 = optimizer.Chromosome(chsize)
    cx = optimizer.OnePointCrossOver()
    newch = cx.crossover(ch1, ch2)
    for i in range(chsize):
        assert newch.realdata[i] == ch1.realdata[i] or newch.realdata[i] == ch2.realdata[i]

def test_twopointcrossover():
    chsize = 10
    ch1 = optimizer.Chromosome(chsize)
    ch2 = optimizer.Chromosome(chsize)
    cx = optimizer.TwoPointCrossOver()
    newch = cx.crossover(ch1, ch2)
    for i in range(chsize):
        assert newch.realdata[i] == ch1.realdata[i] or newch.realdata[i] == ch2.realdata[i]

def test_uniformcrossover():
    chsize = 10
    ch1 = optimizer.Chromosome(chsize)
    ch2 = optimizer.Chromosome(chsize)
    cx = optimizer.UniformCrossOver()
    newch = cx.crossover(ch1, ch2)
    for i in range(chsize):
        assert newch.realdata[i] == ch1.realdata[i] or newch.realdata[i] == ch2.realdata[i]

def test_decode_inc():
    c = optimizer.Chromosome(10)
    c.realdata = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
    permdata = c.decode()
    expected = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(10):
        assert permdata[i] == expected[i]

def test_decode_desc():
    c = optimizer.Chromosome(10)
    c.realdata = np.array([1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])
    permdata = c.decode()
    expected = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    for i in range(10):
        assert permdata[i] == expected[i]

def test_decode_random():
    c = optimizer.Chromosome(10)
    c.realdata = np.array([0.5, 0.1, 0.9, 0.2, 0.8, 0.3, 0.7, 0.4, 0.6, 1.0])
    permdata = c.decode()
    print(permdata)
    expected = [1, 3, 5, 7, 0, 8, 6, 4, 2, 9]
    for i in range(10):
        assert permdata[i] == expected[i]



