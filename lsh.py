
def signature_matrix(matrix, n_signatures):
    SM = []

    for i in range(n_signatures):

        permute = np.arange(np.shape(matrix)[0])

        np.random.shuffle(permute)

        perm_matrix = matrix[permute, :]

        indx = []

        for i in range(perm_matrix.shape[1]):
            indx.append(np.min(perm_matrix.indices[perm_matrix.indptr[i]:perm_matrix.indptr[i + 1]]))

        SM.append(np.array(permute[indx]))

    return np.array(SM)