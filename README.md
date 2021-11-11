# DataMining
Assignment no.2 on similarity alogrithms for Data Mining class
Fall 2021

The purpose of this assignment is to find pairs of most similar users of Netflix with help the LSH technique. There are 3 ways of measuring similarity of two users:

1 Jaccard Similarity (JS). Similarity between two users u1 and u2 is measured by the Jaccard similarity of the sets of movies that they rated, while ratings themselves are irrelevant. Thus, if Si denotes the set of movies rated by the user ui, for i=1, 2, then the similarity between u1 and u2 is #intersect(S1, S2)/#union(S1, S2), where #S denotes the cardinality (the number of elements) of S.

2 Cosine Similarity (CS). Similarity between two users u1 and u2 is measured by the cosine similarity of vectors of ratings given by these two users to movies they rated. Unrated movies are supposed to be rated as 0.

3 Discrete Cosine Similarity (DCS). It is defined as the Cosine Similarity applied to “truncated vectors of ratings”, where every non-zero rating is replaced by 1.
