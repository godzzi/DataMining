import numpy as np
from scipy.sparse import csc_matrix
from numpy import random
import itertools


ratings = np.load("user_movie_rating.npy")
movie_user = csc_matrix((ratings[:, 2], (ratings[:, 1], ratings[:, 0])))[:, 1:]


def bands(sig_matrix, band_num):
    n_rows = (sig_matrix.shape[0]) - ((sig_matrix.shape[0]) % band_num)
    new_sig = sig_matrix[0:n_rows, ]
    r = int((new_sig.shape[0]) / band_num)

    band = []

    for i in range(0, (new_sig.shape[0]), r):
        band.append(new_sig[i:i + r, :].T)
    return np.array(band)


def lsh(sig_matrix, band_num, limit=40):
    buckets = [dict() for _ in range(band_num)]  # create band_num - dictionaries (buckets)

    for idx, band in enumerate(bands(sig_matrix, band_num)):
        for userid, minimum in enumerate(band):

            k = (hash(tuple(minimum)))

            if k not in buckets[idx].keys():
                buckets[idx][k] = [userid]  # create new key
            elif len(buckets[idx][k]) >= limit:
                continue
            else:
                buckets[idx][k].append(userid)  # append user to key

    return buckets


def candidates(buckets, max_size=40):
    cand_pair = []

    for buck in buckets:  # iterate dictionaries
        for k, v in buck.items():
            if len(v) == 1:
                continue
            if len(v) > max_size:
                continue
            else:
                for key in buck.keys():
                    comb = list(itertools.combinations(buck[key], 2))
                    cand_pair.extend(comb)

    return list(set(cand_pair))


def cosine_sim_fun(x, y):
    # x = np.array(x)
    # y = np.array(y)
    xy = np.dot(x, y.T)
    cos_xy = xy / (np.linalg.norm(x) * np.linalg.norm(y))
    alpha = np.rad2deg(np.arccos(cos_xy))
    cossim = 1 - alpha / 180
    return cossim


def random_projections(n_signatures, data):
    v = np.random.randn(n_signatures, data.shape[0])  # random vector v
    h = v * data  # slide 11
    h = np.where(h > 0, 1, h)
    h = np.where(h < 0, -1, h)  # Claim: Prob[h(x)=h(y)] = cosine_sim(x,y)

    return h.astype(int)


def cosine_sim(data, n_signatures=120, band_num=6, threshold=0.73):
    # sm = signature_matrix(data,n_signatures)
    # sm = random_projection.GaussianRandomProjection()
    # sm_new = sm.fit_transform(movie_user)

    sm = random_projections(n_signatures, data)
    buckets = lsh(sm, band_num, limit=10)
    candidate_pairs = candidates(buckets, 10)

    actual_pairs = []

    for a, b in candidate_pairs:
        user1 = data[:, a].toarray().flatten()  # extract ratings from user 1 in one dimension
        user2 = data[:, b].toarray().flatten()  # extract ratings from user 2 in one dimension

        cs = cosine_sim_fun(user1, user2)

        if cs > threshold:
            actual_pairs.append(tuple((a, b)))

    return actual_pairs
